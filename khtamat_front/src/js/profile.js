import '../style/profile.css'

export default function Profile(){
    

return(
    <div className='profile-background'>
        <div className='profile-background-pic'>
            <div className='profile-img-support'>
                <div className='profile-img-div'>
                    <img src={require('../img/Default-Profile-pic.jpg')}className='profile-img'/>
                </div>
            </div>
        </div>
        <div className='profile-information'>
            <div className='information-div'>
                <ul className='ul-info'>
                    <li>
                        <h3 className='h3-fieldtitle'>USER NAME :</h3>
                        <h3 className='h2-fieldtext'>moussa mousselmel</h3>
                    </li>
                    <li>
                        <h3 className='h3-fieldtitle'>EMAIL :</h3>
                        <h3 className='h2-fieldtext'>moussamousselmel@gmail.com</h3>
                    </li>
                </ul>
                <ul className='ul-info'>
                    <li>
                        <h3 className='h3-fieldtitle'>COUNTRY :</h3>
                        <h3 className='h2-fieldtext'>Palestine</h3>
                    </li>
                    <li>
                        <h3 className='h3-fieldtitle'>PASSWORD :</h3>
                        <h3 className='h2-fieldtext'>.........</h3>
                    </li>
                </ul>
            </div>
            <div className='information-div'>
                <ul className='ul-bio'>
                    <li>
                        <h3 className='h3-fieldtitle'>BIO :</h3>
                        <p className='p-fieldtext'>
                            Describe yourself here Describe yourself here
                            Dessadcribe yourself here Describe yourself here
                            Describe yourself here Describe yourself here
                            Describe yourself here Describe yourself here.
                        </p>
                    </li>
                </ul>
            </div>
        </div>
    </div> 
)
}