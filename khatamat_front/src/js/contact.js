import '../style/contact.css';

function Contact() {
    return (
        <div className="contact-back">
            <div className="contact-main">
                <h1 className="contact-title">Contact Us</h1>
                <p className="contact-description">
                    We would love to hear from you! Please fill out the form below, and we will get in touch with you shortly.
                </p>
                <form className="contact-form">
                    <div className="form-group">
                        <label htmlFor="name">Name</label>
                        <input type="text" id="name" name="name" required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input type="email" id="email" name="email" required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="message">Message</label>
                        <textarea id="message" name="message" rows="5" required></textarea>
                    </div>
                    <button type="submit" className="contact-submit">Send Message</button>
                </form>
                <div className="contact-info">
                    <h2>Additional Contact Information</h2>
                    <p>Email: <a href="mailto:info@khatamat.com">info@khatamat.com</a></p>
                    <p>Phone: <a href="tel:+1234567890">+123 456 7890</a></p>
                </div>
            </div>
        </div>
    );
}

export default Contact;
