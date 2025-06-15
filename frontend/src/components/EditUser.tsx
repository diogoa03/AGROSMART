import React, { useState } from 'react';
import './editUser.css';

interface EditUserProps {
  user?: {
    name: string;
    email: string;
  };
  onSave?: (userData: { name: string; password: string; confirmPassword: string }) => void;
  onCancel?: () => void;
}

const EditUser: React.FC<EditUserProps> = ({ 
  user = { name: '', email: '' }, 
  onSave, 
  onCancel 
}) => {
  const [formData, setFormData] = useState({
    name: user.name || '',
    email: user.email || '',
    password: '',
    confirmPassword: ''
  });

  const [errors, setErrors] = useState({
    name: '',
    password: '',
    confirmPassword: ''
  });

  const [touched, setTouched] = useState({
    name: false,
    password: false,
    confirmPassword: false
  });

  const validateName = (name: string): string => {
    if (!name.trim()) {
      return 'Nome é obrigatório';
    }
    if (name.trim().length < 2) {
      return 'Nome deve ter pelo menos 2 caracteres';
    }
    if (name.trim().length > 50) {
      return 'Nome deve ter no máximo 50 caracteres';
    }
    return '';
  };

  const validatePassword = (password: string): string => {
    if (!password) {
      return 'Password é obrigatória';
    }
    if (password.length < 6) {
      return 'Password deve ter pelo menos 6 caracteres';
    }
    if (password.length > 128) {
      return 'Password deve ter no máximo 128 caracteres';
    }
    if (!/(?=.*[a-z])/.test(password)) {
      return 'Password deve conter pelo menos uma letra minúscula';
    }
    if (!/(?=.*[A-Z])/.test(password)) {
      return 'Password deve conter pelo menos uma letra maiúscula';
    }
    if (!/(?=.*\d)/.test(password)) {
      return 'Password deve conter pelo menos um número';
    }
    return '';
  };

  const validateConfirmPassword = (confirmPassword: string, password: string): string => {
    if (!confirmPassword) {
      return 'Confirmação de password é obrigatória';
    }
    if (confirmPassword !== password) {
      return 'As passwords não coincidem';
    }
    return '';
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Validação em tempo real
    if (touched[name as keyof typeof touched]) {
      let error = '';
      
      switch (name) {
        case 'name':
          error = validateName(value);
          break;
        case 'password':
          error = validatePassword(value);
          // Revalidar confirmPassword se já foi tocado
          if (touched.confirmPassword) {
            setErrors(prev => ({
              ...prev,
              confirmPassword: validateConfirmPassword(formData.confirmPassword, value)
            }));
          }
          break;
        case 'confirmPassword':
          error = validateConfirmPassword(value, formData.password);
          break;
      }
      
      setErrors(prev => ({
        ...prev,
        [name]: error
      }));
    }
  };

  const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    const { name } = e.target;
    
    setTouched(prev => ({
      ...prev,
      [name]: true
    }));

    // Validar campo quando perde o foco
    let error = '';
    
    switch (name) {
      case 'name':
        error = validateName(formData.name);
        break;
      case 'password':
        error = validatePassword(formData.password);
        break;
      case 'confirmPassword':
        error = validateConfirmPassword(formData.confirmPassword, formData.password);
        break;
    }
    
    setErrors(prev => ({
      ...prev,
      [name]: error
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Marcar todos os campos como tocados
    setTouched({
      name: true,
      password: true,
      confirmPassword: true
    });

    // Validar todos os campos
    const nameError = validateName(formData.name);
    const passwordError = validatePassword(formData.password);
    const confirmPasswordError = validateConfirmPassword(formData.confirmPassword, formData.password);

    setErrors({
      name: nameError,
      password: passwordError,
      confirmPassword: confirmPasswordError
    });

    // Se não há erros, chamar onSave
    if (!nameError && !passwordError && !confirmPasswordError) {
      onSave?.({
        name: formData.name.trim(),
        password: formData.password,
        confirmPassword: formData.confirmPassword
      });
    }
  };

  const isFormValid = () => {
    return formData.name.trim() && 
           formData.password && 
           formData.confirmPassword &&
           !errors.name && 
           !errors.password && 
           !errors.confirmPassword;
  };

  return (
    <div className="edit-user-container">
      <div className="edit-user-header">
        <button className="menu-button">
          ☰
        </button>
        <img src="/agrosmart-logo.svg" alt="AgroSmart" className="logo" />
      </div>

      <div className="edit-user-content">
        <div className="profile-section">
          <div className="profile-avatar">
            <div className="avatar-circle">
              <div className="avatar-icon"></div>
            </div>
            <button className="change-avatar-btn">Change</button>
          </div>

          <form className="edit-user-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="name">Name</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                onBlur={handleBlur}
                className={errors.name && touched.name ? 'error' : ''}
                placeholder="Digite seu nome"
              />
              {errors.name && touched.name && (
                <span className="error-message">{errors.name}</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                disabled
                className="disabled-field"
                placeholder="Email não pode ser alterado"
              />
              <span className="field-info">O email não pode ser alterado</span>
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                onBlur={handleBlur}
                className={errors.password && touched.password ? 'error' : ''}
                placeholder="Digite sua nova password"
              />
              {errors.password && touched.password && (
                <span className="error-message">{errors.password}</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                onBlur={handleBlur}
                className={errors.confirmPassword && touched.confirmPassword ? 'error' : ''}
                placeholder="Confirme sua password"
              />
              {errors.confirmPassword && touched.confirmPassword && (
                <span className="error-message">{errors.confirmPassword}</span>
              )}
            </div>

            <div className="form-actions">
              <button 
                type="submit" 
                className={`save-btn ${isFormValid() ? 'enabled' : 'disabled'}`}
                disabled={!isFormValid()}
              >
                Save
              </button>
              
              {onCancel && (
                <button 
                  type="button" 
                  className="cancel-btn"
                  onClick={onCancel}
                >
                  Cancel
                </button>
              )}
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default EditUser;