from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination
from .serializers import messageSerializer
from .models import message,groupMembership,group,media
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from drf_spectacular.utils import extend_schema
import mimetypes


class messagePagination(CursorPagination):    
    ordering = "-created_at" 

    
class list_messages(ListAPIView):
    serializer_class = messageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = messagePagination
    
    def get_queryset(self):
        msg_id = self.request.query_params.get('msg_id', None)
        if msg_id != None:
            msg = message.objects.filter(id=msg_id,group=self.kwargs['group_id'],removed=False).first()
            if not msg:
                return message.objects.none()    
            return message.objects.filter(group=self.kwargs['group_id'],created_at__gte = msg.created_at) 
        return message.objects.filter(group=self.kwargs['group_id']) 
    """
    fetches 10 recent created msgs by default
    if a msg_id is specified then fetched msgs starting from that msg
    """
    
    @extend_schema(
        request=None,
        responses={
            200: messageSerializer(many=True),
            403: "Forbidden, user not in group",
            404: "Group not found",
        },
        operation_id="list_messages",
        summary="List Messages",
        description="Retrieve messages for a specific group. If a message ID is provided, messages starting from that message will be retrieved. The user must be a member of the group to view the messages.",
    )
    def get(self,request,*args,**kwargs):
        user = request.user
        group_id = self.kwargs['group_id']
        
        # check user membership in the group 
        is_in_group = groupMembership.objects.filter(group=group_id,user=user).exists()
        if not is_in_group:
            return Response(status=status.HTTP_403_FORBIDDEN,data={"error":"user not in group"})
        return self.list(request,*args,**kwargs)


def validated_file_size(file):
    max_size = 50 * 1024 * 1024  # 50 MB
    if file.size > max_size:
        return False
    return True


supported_mime_types = [
    # Images
    'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml', 'image/bmp', 'image/tiff',
    
    # Videos
    'video/mp4', 'video/mpeg', 'video/quicktime', 'video/x-msvideo', 'video/x-matroska', 'video/webm',
    
    # Audio
    'audio/mpeg', 'audio/ogg', 'audio/wav', 'audio/webm', 'audio/aac', 'audio/mp4', 'audio/x-wav', 'audio/flac',
    
    # Documents
    'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'text/plain',
    
    # Archives
    'application/zip', 'application/x-rar-compressed', 'application/x-7z-compressed', 'application/gzip',
]


def validated_file_type(file):
    mime_type, encoding = mimetypes.guess_type(file.name)
    if mime_type not in supported_mime_types:
        return False
    return True

    
class FileUploadMessage(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
    lookup_field = 'group_id'
    
    @extend_schema(
        request=None,
        responses={
            201: "File uploaded successfully",
            400: "Bad request, invalid data",
            403: "Forbidden, user not in group",
            404: "Group not found",
            406: "Not Acceptable, file too large",
            415: "Unsupported Media Type, file type not supported",
        },
        operation_id="upload_file_message",
        summary="Upload File Message",
        description="Upload a file to a specific group. The user must be a member of the group to upload the file. The file size must not exceed 50 MB and the file type must be supported. Supported file types include images (jpeg, png, gif, webp, svg, bmp, tiff), videos (mp4, mpeg, quicktime, x-msvideo, x-matroska, webm), audio (mpeg, ogg, wav, webm, aac, mp4, x-wav, flac), documents (pdf, msword, openxmlformats-officedocument.wordprocessingml.document, ms-excel, openxmlformats-officedocument.spreadsheetml.sheet, ms-powerpoint, openxmlformats-officedocument.presentationml.presentation, plain text), and archives (zip, x-rar-compressed, x-7z-compressed, gzip).",
    )
    def post(self, request, *args, **kwargs):
        # Extract file and group information
        file = request.FILES['file']
        group_id = self.kwargs['group_id']
        if not validated_file_size(file):
            return Response("file too large",status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if not validated_file_type(file):
            return Response("unsupported media type",status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        
        msg = request.data.get("msg",None)
        reply = request.data.get("reply",None)
        user_mem = request.user.groupMembership.filter(group=group_id).first()
        
        if reply:
            reply = message.objects.filter(id=reply).first() # get the instance
            if not reply:
                return Response("message not found",status=status.HTTP_404_NOT_FOUND)
        
        gr = group.objects.filter(id=group_id).first()
        if not gr:
            return Response("group not found",status=status.HTTP_404_NOT_FOUND)
        
        # Save the file in the Media model
        file = media.objects.create(
            file=file
        )
        msg = message.objects.create(
            group= gr,
            sender= user_mem,
            message= msg,
            reply= reply,
            file=file,
            file_path= file.file.url
        )
        file_type, encoding = mimetypes.guess_type(file.file.path) # get the file type
        # Generate file metadata
        metadata = {
            "id": file.id,
            "url": file.file.url,
            "file_name": file.file.name,
            "file_type": file_type,
            "file_size": file.file.size,
        }

        # Broadcast file metadata via WebSocket
        channel_layer = get_channel_layer()
        group_name = f"chat_{gr.id}"  # Channel Layer group name for the chat
        msg_data = messageSerializer(msg).data
        message_data = {
                    "action": "send_message",
                    "text": msg_data["message"],
                    "time": msg_data["created_at"],
                    "group": msg_data["group"],
                    "id": msg_data['id'] ,
                    "file":metadata,
                    "reply": msg_data["reply"],
                }
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "chat_message",
                "message": message_data,
            },
        )
        return Response(status.HTTP_201_CREATED)

        # Return the file metadata as HTTP response    
    