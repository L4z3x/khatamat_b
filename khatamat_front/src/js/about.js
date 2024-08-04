import '../style/about.css';

function About() {
    return (
        <div className="about-back">
            <div className="about-main">
                <article>
                    <span className='article-title'>What is Khatamat?</span>
                    <p className='about-p'>
                        Khatamat is a unique platform designed to bring together Muslims for the collective goal of worshiping <strong>Allah</strong> and getting closer to him. Here’s a closer look at how it works and its benefits:
                    </p>
                    <div className='about-details'>
                        <div className='detail-item'>
                            <h3>Group Collaboration</h3>
                            <ul>
                                <li><strong>Create and Join Groups:</strong> Users can create or join groups within the platform, dedicated to completing a khatma.</li>
                                <li><strong>Collaborative Reading:</strong> Members work together to ensure every part of the Quran is read within a specified timeframe.</li>
                            </ul>
                        </div>
                        <div className='detail-item'>
                            <h3>Structured Reading</h3>
                            <ul>
                                <li><strong>Organized Reading Schedule:</strong> Groups can set clear schedules, whether for a week or longer, accommodating their needs.</li>
                                <li><strong>Tracking Progress:</strong> Track reading progress and see the collective effort of the group, enhancing motivation.</li>
                            </ul>
                        </div>
                        <div className='detail-item'>
                            <h3>Spiritual Growth</h3>
                            <ul>
                                <li><strong>Shared Experience:</strong> Participating in a khatma with others enhances spiritual unity and purpose.</li>
                                <li><strong>Encouraging Consistency:</strong> Regular group reading helps maintain consistency in spiritual practices.</li>
                            </ul>
                        </div>
                        <div className='detail-item'>
                            <h3>Educational Resources</h3>
                            <ul>
                                <li><strong>Learning Materials:</strong> Access to explanations of Quranic verses and supplementary materials to deepen understanding.</li>
                            </ul>
                        </div>
                        <div className='detail-item'>
                            <h3>Community Building</h3>
                            <ul>
                                <li><strong>Connecting Muslims:</strong> Khatamat helps users connect with fellow Muslims, building a supportive community around Quranic readings.</li>
                            </ul>
                        </div>
                    </div>
                </article>
                
            </div>
        </div>
    );
}

export default About;
