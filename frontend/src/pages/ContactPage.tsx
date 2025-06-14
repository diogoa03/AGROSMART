import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheck, faPaperPlane, faEnvelope, faPhone, faMapMarkerAlt, faClock, faArrowLeft } from '@fortawesome/free-solid-svg-icons';

const ContactPage: React.FC = () => {
    const history = useHistory();
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
        subject: '',
        message: ''
    });
    const [isSubmitted, setIsSubmitted] = useState(false);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Simulação de envio
        setIsSubmitted(true);
        setTimeout(() => {
            setIsSubmitted(false);
            setFormData({
                name: '',
                email: '',
                phone: '',
                subject: '',
                message: ''
            });
        }, 3000);
    };

    const navigateTo = (path: string) => {
        history.push(path);
    };

    return (
        <div className="contact-container">
            <section className="contact-hero">
                <h1 className="section-title">Entre em Contacto Connosco</h1>
                <p className="section-subtitle">Tem questões sobre o AgroSmart? Quer saber mais sobre as nossas soluções? 
                Estamos aqui para ajudar a revolucionar a sua agricultura.</p>
            </section>

            <section className="contact-section">
                <div className="contact-grid">
                    <div className="contact-form-container">
                        <h2 className="form-title">Envie-nos uma Mensagem</h2>
                        
                        {isSubmitted ? (
                            <div className="success-message">
                                <FontAwesomeIcon icon={faCheck} className="success-icon" />
                                <h3>Mensagem Enviada!</h3>
                                <p>Obrigado pelo seu contacto. Responderemos em breve.</p>
                            </div>
                        ) : (
                            <form onSubmit={handleSubmit} className="contact-form">
                                <div className="form-row">
                                    <div className="form-group">
                                        <label htmlFor="name">Nome Completo</label>
                                        <input
                                            type="text"
                                            id="name"
                                            name="name"
                                            value={formData.name}
                                            onChange={handleInputChange}
                                            required
                                            className="form-control"
                                            placeholder="O seu nome"
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="email">Email</label>
                                        <input
                                            type="email"
                                            id="email"
                                            name="email"
                                            value={formData.email}
                                            onChange={handleInputChange}
                                            required
                                            className="form-control"
                                            placeholder="seuemail@exemplo.com"
                                        />
                                    </div>
                                </div>

                                <div className="form-row">
                                    <div className="form-group">
                                        <label htmlFor="phone">Telefone</label>
                                        <input
                                            type="tel"
                                            id="phone"
                                            name="phone"
                                            value={formData.phone}
                                            onChange={handleInputChange}
                                            className="form-control"
                                            placeholder="+351 912 345 678"
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="subject">Assunto</label>
                                        <select
                                            id="subject"
                                            name="subject"
                                            value={formData.subject}
                                            onChange={handleInputChange}
                                            required
                                            className="form-control"
                                        >
                                            <option value="">Selecione um assunto</option>
                                            <option value="demo">Demonstração do Produto</option>
                                            <option value="pricing">Informações sobre Preços</option>
                                            <option value="support">Suporte Técnico</option>
                                            <option value="partnership">Parcerias</option>
                                            <option value="other">Outro</option>
                                        </select>
                                    </div>
                                </div>

                                <div className="form-group">
                                    <label htmlFor="message">Mensagem</label>
                                    <textarea
                                        id="message"
                                        name="message"
                                        value={formData.message}
                                        onChange={handleInputChange}
                                        required
                                        rows={6}
                                        className="form-control"
                                        placeholder="Descreva como podemos ajudar..."
                                    />
                                </div>

                                <button
                                    type="submit"
                                    className="submit-button"
                                >
                                    <FontAwesomeIcon icon={faPaperPlane} className="send-icon" />
                                    <span>Enviar Mensagem</span>
                                </button>
                            </form>
                        )}
                    </div>

                    <div className="contact-info-container">
                        <div className="info-card">
                            <h3>Informações de Contacto</h3>
                            
                            <div className="info-item">
                                <div className="info-icon-container">
                                    <FontAwesomeIcon icon={faEnvelope} className="info-icon" />
                                </div>
                                <div className="info-content">
                                    <h4>Email</h4>
                                    <p>contacto@agrosmart.pt</p>
                                    <p>suporte@agrosmart.pt</p>
                                </div>
                            </div>

                            <div className="info-item">
                                <div className="info-icon-container">
                                    <FontAwesomeIcon icon={faPhone} className="info-icon" />
                                </div>
                                <div className="info-content">
                                    <h4>Telefone</h4>
                                    <p>+351 234 567 890</p>
                                    <p>+351 912 345 678</p>
                                </div>
                            </div>

                            <div className="info-item">
                                <div className="info-icon-container">
                                    <FontAwesomeIcon icon={faMapMarkerAlt} className="info-icon" />
                                </div>
                                <div className="info-content">
                                    <h4>Morada</h4>
                                    <p>
                                        Rua da Inovação, 123<br />
                                        3810-193 Aveiro<br />
                                        Portugal
                                    </p>
                                </div>
                            </div>

                            <div className="info-item">
                                <div className="info-icon-container">
                                    <FontAwesomeIcon icon={faClock} className="info-icon" />
                                </div>
                                <div className="info-content">
                                    <h4>Horário</h4>
                                    <p>
                                        Segunda a Sexta: 9h00 - 18h00<br />
                                        Sábado: 9h00 - 13h00<br />
                                        Domingo: Fechado
                                    </p>
                                </div>
                            </div>
                        </div>
                        
                        {/* FAQ Section */}
                        <div className="faq-card">
                            <h3>Perguntas Frequentes</h3>
                            
                            <div className="faq-item">
                                <h4>Como funciona o AgroSmart?</h4>
                                <p>
                                    O AgroSmart combina sensores IoT, dados meteorológicos e IA para 
                                    fornecer informações precisas sobre as suas culturas.
                                </p>
                            </div>

                            <div className="faq-item">
                                <h4>Existe um período de teste gratuito?</h4>
                                <p>
                                    Sim, oferecemos 30 dias de teste gratuito para conhecer 
                                    todas as funcionalidades da plataforma.
                                </p>
                            </div>

                            <div className="faq-item">
                                <h4>Que tipo de culturas são suportadas?</h4>
                                <p>
                                    Suportamos uma vasta gama de culturas, desde cereais a 
                                    hortícolas, fruteiras e vinhas.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <div className="back-button-container">
                <button className="back-button" onClick={() => navigateTo('/agrosmart')}>
                    <FontAwesomeIcon icon={faArrowLeft} className="back-icon" />
                    Voltar para HomePage
                </button>
            </div>
        </div>
    );
};

export default ContactPage;