import React , { useEffect ,useState,useRef } from 'react';
import '../style/dashboard.css'

function DashBoard(){
   
    const [part , setPart] = useState([])  // <--- for storing part that are clicked.
    const partRefs = useRef([])
    const [time,setTime]= useState({
        sec: 8,
        min:0,
        hour: 0,
        day: 0
    })
    const [info,setInfo] = useState([' من سورة البقرة  1 الى 35'])   // TODO: add all infos about each part.
    const [inf,setInf] = useState('')
    //const [inf_style,setInf_style] = useState({})
    useEffect(()=>{setTimeout(()=>{   // <--- timer function:
        setTime(prevTime => {
            let newTime = { ...prevTime };
            if (newTime.day <= 0 && newTime.hour <= 0 && newTime.min <= 0 && newTime.sec <= 0 ) {  
            } else {
                newTime.sec--;
                if (newTime.sec === -1) {
                    newTime.min--;
                    newTime.sec = 59;
                    if (newTime.min === -1) {
                        newTime.hour--;
                        newTime.min = 59;
                        if (newTime.hour === -1) {
                            newTime.day--;
                            newTime.hour = 23;
                        }
                    }
                }
            }
            return newTime;
        });},1000)});
                                    // <--- setting the time variable:
        let clock_day  = time.day > 9 ? ` ${time.day}`  : ` 0${time.day}` 
        let clock_hour = time.hour > 9 ? ` ${time.hour}` : ` 0${time.hour}` 
        let clock_min = time.min > 9 ? ` ${time.min}` : ` 0${time.min}`  
        let clock_sec = time.sec > 9 ? ` ${time.sec}`: ` 0${time.sec}` 
        let clock = clock_day + ` day` + clock_hour + ` Hour`+ clock_min +` min`+ clock_sec+` sec`
    
    
    const handleSpanClick =(e,i)=>{       // <--- setting the onclick fun for the child (span).
        partRefs.current[i].click();
        e.stopPropagation();
    }
                                    
    const handlePartOnclick = (e)=>{        // <--- setting the onclick function.
        if (e.target.className === 'part') {
            const newPart = e.target.childNodes[0].innerText; 
            if (e.target.style.opacity === '' || !part.includes(newPart)) {
                setPart(value =>([...value,newPart]));
                e.target.style.opacity = 0.45 ;        // <--- change opacity on click and add part.
            }else{
                e.target.style.opacity ='';
                setPart(value=>(value.filter(value => value !== newPart)))
            }
        }
        e.stopPropagation();   
    }
    useEffect(()=>{
        console.log(part);
    },[part]);

    const showInfoOnHover = (e,i)=>{                    // <--- on click (info icon) : add the info.
        const curPart = partRefs.current[i];
        const info = partRefs.current[i].lastChild;
       console.log(info);
        if ( info.style.display === '') {
            info.style.display = 'flex';  
            info.style.opacity = 1;
            const container_bounding = curPart.parentNode.getBoundingClientRect();    
            const info_bounding = info.getBoundingClientRect();
            if (info_bounding.right > container_bounding.right) {
                const overflow = info_bounding.right - container_bounding.right;
                info.style.left = `-${overflow}px`
            }                                        
        }                                         
    }

    const handleMouseLeave = (e,i)=>{       // on mouse leave (info icon) : remove the info.
        const curPart = partRefs.current[i];
        if (curPart.lastChild.style.display === 'flex') {
            curPart.lastChild.style.display = null ;
        }
    }

        return(
        <div className='dash-backround'>
            <div className='timer'>
                <h1>Time Left:&nbsp;&nbsp;</h1><h1 className='time'>{clock}</h1>
            </div>
            <div style={{flexDirection: "column"}}className='part-container'>
                <h2 style={{fontFamily: "kufam",marginBottom: "0px"}}>اختر جزءا من القرآن و اتله قبل نهاية الوقت</h2>
                <h2>pick parts from the quran and read it before the time ends</h2>
            </div>
            <div className='part-container'>
                {Array.from({ length: 60 }, (_, i) => (                                 // <--- this part is from chatgpt i don't get the syntax yet ... 
                    <div ref={el => partRefs.current[i] = el} key={i} className='part'  //           shhhh don't tell anyone okey ...
                    onClick={(e) => handlePartOnclick(e)}>
                        <div className='part-default'>
                            <span className='span-part' onClick={(e) => handleSpanClick(e, i)}>الحزب  {i + 1}</span>
                            <img onMouseOver={(e)=>showInfoOnHover(e,i)} onMouseLeave={(e)=>handleMouseLeave(e,i)}className='info-icon' src={require('../img/info.png')} 
                            alt='info-icon' />
                        </div> 
                        <div className='info-div'><span dir="rtl" lang='ar' className='info-span'>من &nbsp;سورة &nbsp;البقرة &nbsp;الآية &nbsp; 1&nbsp; إلى&nbsp; الآية&nbsp; 35&nbsp;</span></div> 
                    </div>                              // TODO: replace the text with the info variable.
                ))}
            </div>
        </div>
    )
}

export default DashBoard;