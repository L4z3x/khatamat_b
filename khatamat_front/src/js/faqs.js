import React from 'react';
import '../style/faqs.css';

export default function FAQs() {
    return (
        <div className="faqs-container">
            <h1 className="faqs-title">Frequently Asked Questions</h1>
            <div className="faqs-content">
                <div className="faq-item">
                    <h2 className="faq-question">What is Khatamat?</h2>
                    <p className="faq-answer">
                        Khatamat is a platform that brings together Muslims to read and complete the Holy Quran collectively, known as khatmas.
                    </p>
                </div>
                <div className="faq-item">
                    <h2 className="faq-question">How do I join a Khatma?</h2>
                    <p className="faq-answer">
                        To join a Khatma, you need to sign up for an account, log in, and explore the available Khatma groups or create a new one.
                    </p>
                </div>
                <div className="faq-item">
                    <h2 className="faq-question">Can I create my own Khatma group?</h2>
                    <p className="faq-answer">
                        Yes, once you are registered and logged in, you can create your own Khatma group and invite others to join.
                    </p>
                </div>
                <div className="faq-item">
                    <h2 className="faq-question">Is Khatamat free to use?</h2>
                    <p className="faq-answer">
                        Yes, Khatamat is completely free to use. Our goal is to help Muslims connect and complete the Quran together.
                    </p>
                </div>
                <div className="faq-item">
                    <h2 className="faq-question">What is a Khatma?</h2>
                    <p className="faq-answer">
                        A Khatma involves choosing a part of the Holy Quran or the entire Quran to be read by a group of people or an individual within a specific period (e.g., a week).
                    </p>
                </div>
                <div className="faq-item">
                    <h2 className="faq-question">How can I contact the Khatamat team?</h2>
                    <p className="faq-answer">
                        You can contact us via the <a href="/contact" className="faq-link">Contact Us</a> page for any questions or support.
                    </p>
                </div>
            </div>
        </div>
    );
}
