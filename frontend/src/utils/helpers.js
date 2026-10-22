/**
 * Yardımcı Fonksiyonlar
 */

import { STATUS_COLORS, PRIORITY_COLORS } from './constants';

/**
 * Tarih formatla (Türkçe)
 */
export const formatDate = (dateString) => {
  const date = new Date(dateString);
  const now = new Date();
  const diff = now - date;
  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (days > 7) {
    return date.toLocaleDateString('tr-TR', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } else if (days > 0) {
    return `${days} gün önce`;
  } else if (hours > 0) {
    return `${hours} saat önce`;
  } else if (minutes > 0) {
    return `${minutes} dakika önce`;
  } else {
    return 'Az önce';
  }
};

/**
 * Durum rengini al - Damga Renkleri
 */
export const getStatusColor = (status) => {
  return STATUS_COLORS[status] || '#6b7280';
};

/**
 * Öncelik rengini al
 */
export const getPriorityColor = (priority) => {
  return PRIORITY_COLORS[priority] || '#6b7280';
};

/**
 * Toast bildirimi göster - Form İzlenim
 */
export const showToast = (message, type = 'info') => {
  const toast = document.createElement('div');
  toast.textContent = message;
  
  const colors = {
    success: '#2F6B4F',
    error: '#C1440E',
    info: '#3B5998'
  };
  
  toast.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 14px 24px;
    background: ${colors[type] || colors.info};
    color: white;
    border-radius: 6px;
    box-shadow: 0 4px 12px rgba(27, 42, 74, 0.2);
    z-index: 10000;
    font-family: 'Archivo', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border: 3px solid currentColor;
    animation: slideIn 0.3s ease-out;
  `;
  
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease-in';
    setTimeout(() => document.body.removeChild(toast), 300);
  }, 3000);
};
