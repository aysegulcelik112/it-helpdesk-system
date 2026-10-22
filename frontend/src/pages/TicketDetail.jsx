/**
 * Talep Detay Sayfası
 */

import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ticketsAPI, commentsAPI } from '../services/api';
import { showToast, formatDate, getStatusColor, getPriorityColor } from '../utils/helpers';
import { isITStaff } from '../utils/auth';
import Navbar from '../components/Navbar';
import '../styles/TicketDetail.css';

function TicketDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [ticket, setTicket] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadTicket();
    loadComments();
  }, [id]);

  const loadTicket = async () => {
    try {
      const response = await ticketsAPI.getById(id);
      setTicket(response.data);
    } catch (error) {
      showToast('Talep yüklenirken hata oluştu', 'error');
      navigate(-1);
    } finally {
      setLoading(false);
    }
  };

  const loadComments = async () => {
    try {
      const response = await commentsAPI.list(id);
      setComments(response.data);
    } catch (error) {
      console.error('Yorumlar yüklenemedi', error);
    }
  };

  const handleAddComment = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;

    setSubmitting(true);
    try {
      await commentsAPI.create(id, newComment);
      setNewComment('');
      loadComments();
      showToast('Yorum eklendi', 'success');
    } catch (error) {
      showToast('Yorum eklenirken hata oluştu', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  const handleStatusChange = async (newStatus) => {
    try {
      await ticketsAPI.update(id, { status: newStatus });
      showToast('Durum güncellendi', 'success');
      loadTicket();
    } catch (error) {
      showToast('Durum güncellenirken hata oluştu', 'error');
    }
  };

  const handlePriorityChange = async (newPriority) => {
    try {
      await ticketsAPI.update(id, { priority: newPriority });
      showToast('Öncelik güncellendi', 'success');
      loadTicket();
    } catch (error) {
      showToast('Öncelik güncellenirken hata oluştu', 'error');
    }
  };

  const handleAssignToMe = async () => {
    try {
      await ticketsAPI.assignToMe(id);
      showToast('Talep size atandı', 'success');
      loadTicket();
    } catch (error) {
      showToast('Atama yapılırken hata oluştu', 'error');
    }
  };

  const handleClose = async () => {
    if (!confirm('Bu talebi kapatmak istediğinizden emin misiniz?')) return;
    
    try {
      await ticketsAPI.close(id);
      showToast('Talep kapatıldı', 'success');
      loadTicket();
    } catch (error) {
      showToast('Talep kapatılırken hata oluştu', 'error');
    }
  };

  if (loading) {
    return (
      <div className="dashboard">
        <Navbar />
        <div className="loading">Yükleniyor...</div>
      </div>
    );
  }

  if (!ticket) return null;

  return (
    <div className="dashboard">
      <Navbar />
      
      <div className="ticket-detail-container">
        <button className="back-button" onClick={() => navigate(-1)}>
          ← Geri
        </button>

        <div className="ticket-detail-content">
          <div className="ticket-main">
            <div className="ticket-detail-header">
              <div>
                <span className="ticket-id-large">Talep #{ticket.id}</span>
                <h1>{ticket.title}</h1>
              </div>
              <span className="ticket-status-large" style={{backgroundColor: getStatusColor(ticket.status)}}>
                {ticket.status}
              </span>
            </div>

            <div className="ticket-info-grid">
              <div className="info-item">
                <span className="info-label">Kategori</span>
                <span className="info-value">📂 {ticket.category}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Öncelik</span>
                <span className="info-value" style={{color: getPriorityColor(ticket.priority)}}>
                  ⚡ {ticket.priority}
                </span>
              </div>
              <div className="info-item">
                <span className="info-label">Oluşturan</span>
                <span className="info-value">{ticket.creator.full_name}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Atanan</span>
                <span className="info-value">
                  {ticket.assigned_to_user ? ticket.assigned_to_user.full_name : 'Atanmadı'}
                </span>
              </div>
              <div className="info-item">
                <span className="info-label">Oluşturma</span>
                <span className="info-value">{formatDate(ticket.created_at)}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Güncelleme</span>
                <span className="info-value">{formatDate(ticket.updated_at)}</span>
              </div>
            </div>

            <div className="ticket-description">
              <h3>Açıklama</h3>
              <p>{ticket.description}</p>
            </div>

            <div className="comments-section">
              <h3>Yorumlar ({comments.length})</h3>
              
              <form onSubmit={handleAddComment} className="comment-form">
                <textarea
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  placeholder="Yorum ekleyin..."
                  rows={3}
                  disabled={submitting}
                />
                <button type="submit" disabled={submitting || !newComment.trim()}>
                  {submitting ? 'Gönderiliyor...' : 'Yorum Ekle'}
                </button>
              </form>

              <div className="comments-list">
                {comments.map(comment => (
                  <div key={comment.id} className="comment">
                    <div className="comment-header">
                      <strong>{comment.author.full_name}</strong>
                      <span className="comment-date">{formatDate(comment.created_at)}</span>
                    </div>
                    <p>{comment.message}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {isITStaff() && (
            <div className="ticket-sidebar">
              <div className="sidebar-section">
                <h4>Durum Değiştir</h4>
                <select 
                  value={ticket.status} 
                  onChange={(e) => handleStatusChange(e.target.value)}
                  className="status-select"
                >
                  <option value="Açık">Açık</option>
                  <option value="İşleme Alındı">İşleme Alındı</option>
                  <option value="Beklemede">Beklemede</option>
                  <option value="Çözüldü">Çözüldü</option>
                  <option value="Kapatıldı">Kapatıldı</option>
                </select>
              </div>

              <div className="sidebar-section">
                <h4>Öncelik Değiştir</h4>
                <select 
                  value={ticket.priority} 
                  onChange={(e) => handlePriorityChange(e.target.value)}
                  className="priority-select"
                >
                  <option value="Düşük">Düşük</option>
                  <option value="Orta">Orta</option>
                  <option value="Yüksek">Yüksek</option>
                  <option value="Acil">Acil</option>
                </select>
              </div>

              {!ticket.assigned_to_user && (
                <button className="assign-button" onClick={handleAssignToMe}>
                  Kendime Ata
                </button>
              )}
            </div>
          )}

          {!isITStaff() && ticket.status === 'Çözüldü' && (
            <div className="ticket-sidebar">
              <div className="sidebar-section">
                <h4>Talep Çözüldü</h4>
                <p style={{fontSize: '0.875rem', color: 'var(--color-text-secondary)', marginBottom: '1rem'}}>
                  Sorununuz çözüldüyse talebi kapatabilirsiniz.
                </p>
                <button className="close-button-full" onClick={handleClose}>
                  Talebi Kapat
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default TicketDetail;
