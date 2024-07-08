import '../style/about.css'
function About () {
    return(
        <div className="about-back">
            <div className="about-main">
                <article>
                    <span className='article-title'>What is  Khatamat ?</span>
                    <p className='about-p'>Khatamat is a hub-like website that
                     allow you to create a group with others and do a <strong>khatma</strong> together .</p>
                </article>                          {/*TODO: add that # in the url when khatma is clicked.  */}
                <article>
                    
                <span className='article-title'>What is a Khatma ?</span>
                    <p className='about-p'>A khatma is choosing a part of the Holy Quran or all of it 
                    to be read by a group of people or a single one, and that should be in a known period of time (ex : week). </p>
                </article>
                <article>
                    <span className='article-title'>Need an example ?</span>
                    <p className='about-p'>a group of 30 person decided to do a khatma of the hole Quran in a week
                    ,each person will take his part(s) to read it, the hole khatma is devided to 
                    even part and that part could be a <strong>
                    <a className='about-p' href='https://en.wikipedia.org/wiki/Juz%27#Hizbs'target="_blank" rel="noopener noreferrer">hizb</a></strong> or
                    &nbsp;<strong><a className='about-p' href='https://en.wikipedia.org/wiki/Juz%27#Hizbs'target="_blank" rel="noopener noreferrer">Juz'</a>
                    </strong> or more.</p>
                </article>
            </div>
        </div>
    )
}
export default About;