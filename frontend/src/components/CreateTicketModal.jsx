/**
 * Talep Oluşturma Modal
 */

import { useState } from 'react';
import { ticketsAPI } from '../services/api';
import { TICKET_CATEGORIES, TICKET_PRIORITIES } from '../utils/constants';
import { showToast } from '../utils/helpers';
import '../styles/Modal.css';

function CreateTicketModal({ onClose, onSuccess }) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'Yazılım',
    priority: 'Orta'
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await ticketsAPI.create(formData);
      onSuccess();
    } catch (error) {
      showToast(error.response?.data?.detail || 'Talep oluşturulamadı', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Yeni Destek Talebi</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Başlık *</label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => setFormData({...formData, title: e.target.value})}
              placeholder="Sorununuzu kısaca özetleyin"
              required
              minLength={5}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Kategori *</label>
              <select
                value={formData.category}
                onChange={(e) => setFormData({...formData, category: e.target.value})}
                required
              >
                {Object.values(TICKET_CATEGORIES).map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Öncelik *</label>
              <select
                value={formData.priority}
                onChange={(e) => setFormData({...formData, priority: e.target.value})}
                required
              >
                {Object.values(TICKET_PRIORITIES).map(priority => (
                  <option key={priority} value={priority}>{priority}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-group">
            <label>Detaylı Açıklama *</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              placeholder="Sorununuzu detaylı bir şekilde açıklayın..."
              rows={6}
              required
              minLength={10}
            />
          </div>

          <div className="modal-actions">
            <button type="button" onClick={onClose} className="cancel-button">
              İptal
            </button>
            <button type="submit" className="submit-button" disabled={loading}>
              {loading ? 'Oluşturuluyor...' : 'Talep Oluştur'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default CreateTicketModal;
