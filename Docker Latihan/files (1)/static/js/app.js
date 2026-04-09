/* ═══════════════════════════════════════════════════════════
   NexDrive — Main JavaScript
═══════════════════════════════════════════════════════════ */

// ─── Toast auto-dismiss ──────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.toast').forEach(t => {
    setTimeout(() => t.style.animation = 'slideIn .3s ease reverse', 3500);
    setTimeout(() => t.remove(), 3800);
  });
});

// ─── Sidebar ─────────────────────────────────────────────
function toggleSidebar() {
  const sb = document.getElementById('sidebar');
  const ov = document.getElementById('sidebarOverlay');
  sb.classList.toggle('open');
  ov.classList.toggle('active');
}

// ─── Modal Helpers ────────────────────────────────────────
function openModal(id) { document.getElementById(id).classList.add('active'); }
function closeModal(id) { document.getElementById(id).classList.remove('active'); }

// Close modal on backdrop click
document.addEventListener('click', e => {
  if (e.target.classList.contains('modal')) {
    e.target.classList.remove('active');
  }
});
// Close on Escape
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal.active').forEach(m => m.classList.remove('active'));
  }
});

// ─── Upload Modal ─────────────────────────────────────────
let uploadQueue = [];

function openUploadModal() {
  uploadQueue = [];
  document.getElementById('fileQueue').innerHTML = '';
  document.getElementById('uploadBtn').disabled = true;
  document.getElementById('fileInput').value = '';
  openModal('uploadModal');
}

function openFolderModal() {
  setTimeout(() => document.getElementById('folderNameInput')?.focus(), 100);
  openModal('folderModal');
}

// Drag & Drop
const dropZone = document.getElementById('dropZone');
if (dropZone) {
  ['dragenter','dragover'].forEach(ev => {
    dropZone.addEventListener(ev, e => { e.preventDefault(); dropZone.classList.add('drag-over'); });
  });
  ['dragleave','drop'].forEach(ev => {
    dropZone.addEventListener(ev, e => { e.preventDefault(); dropZone.classList.remove('drag-over'); });
  });
  dropZone.addEventListener('drop', e => addToQueue(e.dataTransfer.files));
  document.getElementById('fileInput')?.addEventListener('change', e => addToQueue(e.target.files));
}

function humanSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
  if (bytes < 1073741824) return (bytes / 1048576).toFixed(1) + ' MB';
  return (bytes / 1073741824).toFixed(1) + ' GB';
}

function getFileIcon(name) {
  const ext = name.split('.').pop().toLowerCase();
  const icons = {
    jpg:'fa-image',jpeg:'fa-image',png:'fa-image',gif:'fa-image',webp:'fa-image',svg:'fa-image',
    mp4:'fa-film',avi:'fa-film',mov:'fa-film',mkv:'fa-film',webm:'fa-film',
    mp3:'fa-music',wav:'fa-music',flac:'fa-music',ogg:'fa-music',aac:'fa-music',
    pdf:'fa-file-pdf',doc:'fa-file-word',docx:'fa-file-word',xls:'fa-file-excel',xlsx:'fa-file-excel',
    ppt:'fa-file-powerpoint',pptx:'fa-file-powerpoint',txt:'fa-file-alt',
    zip:'fa-file-archive',rar:'fa-file-archive','7z':'fa-file-archive',tar:'fa-file-archive',
    py:'fa-code',js:'fa-code',ts:'fa-code',html:'fa-code',css:'fa-code',json:'fa-code',
  };
  return icons[ext] || 'fa-file';
}

function addToQueue(files) {
  const queueEl = document.getElementById('fileQueue');
  Array.from(files).forEach(file => {
    if (uploadQueue.find(f => f.name === file.name && f.size === file.size)) return;
    uploadQueue.push(file);
    const div = document.createElement('div');
    div.className = 'queue-item';
    div.id = `qi-${uploadQueue.length - 1}`;
    div.innerHTML = `
      <i class="fa ${getFileIcon(file.name)}" style="color:#6366f1"></i>
      <div class="queue-info">
        <div class="queue-name">${file.name}</div>
        <div class="queue-size">${humanSize(file.size)}</div>
      </div>
      <span class="queue-status" id="qs-${uploadQueue.length - 1}"></span>
      <button class="queue-remove" onclick="removeFromQueue(${uploadQueue.length - 1}, this)">
        <i class="fa fa-times"></i>
      </button>`;
    queueEl.appendChild(div);
  });
  document.getElementById('uploadBtn').disabled = uploadQueue.filter(Boolean).length === 0;
}

function removeFromQueue(idx, btn) {
  uploadQueue[idx] = null;
  btn.closest('.queue-item').remove();
  document.getElementById('uploadBtn').disabled = uploadQueue.filter(Boolean).length === 0;
}

async function startUpload() {
  const files = uploadQueue.filter(Boolean);
  if (!files.length) return;
  const btn = document.getElementById('uploadBtn');
  btn.disabled = true;
  btn.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Mengupload...';

  const folderId = document.getElementById('currentFolderId')?.value || '';
  const formData = new FormData();
  files.forEach((f, i) => { formData.append('files', f); });
  if (folderId) formData.append('folder_id', folderId);

  uploadQueue.forEach((f, i) => {
    if (f) {
      const s = document.getElementById(`qs-${i}`);
      if (s) { s.innerHTML = '<i class="fa fa-spinner fa-spin"></i>'; s.className = 'queue-status'; }
    }
  });

  try {
    const res = await fetch('/upload', { method: 'POST', body: formData });
    const data = await res.json();
    if (data.uploaded) {
      data.uploaded.forEach(u => showNotify('success', `${u.name} berhasil diupload`));
    }
    if (data.errors) {
      data.errors.forEach(e => showNotify('error', e));
    }
    setTimeout(() => { closeModal('uploadModal'); location.reload(); }, 800);
  } catch (err) {
    showNotify('error', 'Upload gagal: ' + err.message);
    btn.disabled = false;
    btn.innerHTML = '<i class="fa fa-upload"></i> Upload Sekarang';
  }
}

// ─── Notifications ────────────────────────────────────────
function showNotify(type, msg) {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    container.id = 'toastContainer';
    document.body.appendChild(container);
  }
  const icons = { success: 'fa-check-circle', error: 'fa-times-circle', info: 'fa-info-circle' };
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<i class="fa ${icons[type] || icons.info}"></i><span>${msg}</span><button onclick="this.parentElement.remove()"><i class="fa fa-times"></i></button>`;
  container.appendChild(toast);
  setTimeout(() => { toast.style.animation = 'slideIn .3s ease reverse'; }, 3500);
  setTimeout(() => toast.remove(), 3800);
}

// ─── Star Toggle ──────────────────────────────────────────
async function toggleStar(fileId, btn) {
  try {
    const res = await fetch(`/file/${fileId}/star`, { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      btn.classList.toggle('starred', data.starred);
      showNotify('info', data.starred ? 'File ditandai ⭐' : 'Tanda bintang dihapus');
    }
  } catch (e) { showNotify('error', 'Gagal mengubah status bintang'); }
}

// ─── Rename ───────────────────────────────────────────────
let _renameTarget = null;

function openRenameFile(fileId, name) {
  _renameTarget = { type: 'file', id: fileId };
  document.getElementById('renameInput').value = name;
  openModal('renameModal');
  setTimeout(() => document.getElementById('renameInput').focus(), 100);
}

function openRenameFolder(folderId, name) {
  _renameTarget = { type: 'folder', id: folderId };
  document.getElementById('renameInput').value = name;
  openModal('renameModal');
  setTimeout(() => document.getElementById('renameInput').focus(), 100);
}

async function submitRename() {
  const newName = document.getElementById('renameInput').value.trim();
  if (!newName || !_renameTarget) return;
  const url = _renameTarget.type === 'file' ? `/file/${_renameTarget.id}/rename` : `/folder/${_renameTarget.id}/rename`;
  const form = new FormData();
  form.append('name', newName);
  try {
    const res = await fetch(url, { method: 'POST', body: form });
    const data = await res.json();
    if (data.success) {
      showNotify('success', 'Berhasil diganti nama');
      closeModal('renameModal');
      setTimeout(() => location.reload(), 500);
    }
  } catch (e) { showNotify('error', 'Gagal mengganti nama'); }
}

// Enter key in rename input
document.getElementById('renameInput')?.addEventListener('keydown', e => {
  if (e.key === 'Enter') submitRename();
});

// ─── Delete ───────────────────────────────────────────────
let _deleteTarget = null;

function openDeleteFile(fileId, name) {
  _deleteTarget = { type: 'file', id: fileId };
  document.getElementById('deleteTargetName').textContent = name;
  openModal('deleteModal');
}

function openDeleteFolder(folderId, name) {
  _deleteTarget = { type: 'folder', id: folderId };
  document.getElementById('deleteTargetName').textContent = `folder "${name}" beserta isinya`;
  openModal('deleteModal');
}

async function confirmDelete() {
  if (!_deleteTarget) return;
  if (_deleteTarget.type === 'file') {
    try {
      const res = await fetch(`/file/${_deleteTarget.id}/delete`, { method: 'POST' });
      const data = await res.json();
      if (data.success) {
        showNotify('success', 'File berhasil dihapus');
        closeModal('deleteModal');
        setTimeout(() => location.reload(), 500);
      }
    } catch (e) { showNotify('error', 'Gagal menghapus file'); }
  } else {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/folder/${_deleteTarget.id}/delete`;
    document.body.appendChild(form);
    form.submit();
  }
}

// ─── Share ────────────────────────────────────────────────
let _shareFileId = null;

function openShareModal(fileId, isShared, token) {
  _shareFileId = fileId;
  const urlWrap = document.getElementById('shareUrlWrap');
  const unshareBtn = document.getElementById('unshareBtn');
  
  if (isShared && token) {
    const shareUrl = `${window.location.origin}/share/${token}`;
    document.getElementById('shareUrlInput').value = shareUrl;
    urlWrap.style.display = 'flex';
    unshareBtn.style.display = 'inline-flex';
  } else {
    urlWrap.style.display = 'none';
    unshareBtn.style.display = 'none';
  }
  openModal('shareModal');
}

async function doShare(action) {
  if (!_shareFileId) return;
  const form = new FormData();
  form.append('action', action);
  try {
    const res = await fetch(`/file/${_shareFileId}/share`, { method: 'POST', body: form });
    const data = await res.json();
    if (data.success) {
      if (action === 'share') {
        document.getElementById('shareUrlInput').value = data.url;
        document.getElementById('shareUrlWrap').style.display = 'flex';
        document.getElementById('unshareBtn').style.display = 'inline-flex';
        showNotify('success', 'Link berbagi dibuat!');
      } else {
        document.getElementById('shareUrlWrap').style.display = 'none';
        document.getElementById('unshareBtn').style.display = 'none';
        showNotify('info', 'Link berbagi dihapus');
        setTimeout(() => closeModal('shareModal'), 800);
      }
    }
  } catch (e) { showNotify('error', 'Gagal memproses permintaan'); }
}

function copyShareUrl() {
  const input = document.getElementById('shareUrlInput');
  navigator.clipboard.writeText(input.value).then(() => {
    showNotify('success', 'Link disalin ke clipboard!');
  }).catch(() => {
    input.select();
    document.execCommand('copy');
    showNotify('success', 'Link disalin!');
  });
}

// ─── Preview ──────────────────────────────────────────────
async function openPreview(fileId) {
  document.getElementById('previewTitle').innerHTML = '<i class="fa fa-spinner fa-spin"></i> Memuat...';
  document.getElementById('previewBody').innerHTML = '<div class="preview-loading"><i class="fa fa-spinner fa-spin"></i></div>';
  openModal('previewModal');
  
  try {
    const res = await fetch(`/file/${fileId}/preview`);
    const data = await res.json();
    document.getElementById('previewTitle').innerHTML = `<i class="fa fa-eye"></i> ${data.name}`;
    
    let html = '';
    const type = data.type;
    const mime = data.mime || '';
    
    if (type === 'image') {
      html = `<img src="${data.url}" alt="${data.name}" loading="lazy">`;
    } else if (type === 'video') {
      html = `<video controls autoplay style="max-height:60vh"><source src="${data.url}" type="${mime}">Video tidak didukung browser.</video>`;
    } else if (type === 'audio') {
      html = `<audio controls autoplay style="width:100%"><source src="${data.url}" type="${mime}">Audio tidak didukung browser.</audio>`;
    } else if (mime === 'application/pdf') {
      html = `<iframe src="${data.url}" class="preview-iframe"></iframe>`;
    } else if (type === 'code' || mime.startsWith('text/')) {
      html = `<iframe src="${data.url}" class="preview-iframe" style="background:#1a1e2a"></iframe>`;
    } else {
      html = `<div class="preview-no-preview">
        <i class="fa fa-file" style="color:#6366f1"></i>
        <p>Preview tidak tersedia untuk tipe file ini.</p>
        <a href="/file/${fileId}/download" class="btn-primary"><i class="fa fa-download"></i> Unduh File</a>
      </div>`;
    }
    document.getElementById('previewBody').innerHTML = html;
  } catch (e) {
    document.getElementById('previewBody').innerHTML = '<div class="preview-no-preview"><i class="fa fa-times-circle" style="color:#ef4444"></i><p>Gagal memuat preview.</p></div>';
  }
}

// ─── Password Toggle ──────────────────────────────────────
function togglePw(inputId, btn) {
  const input = document.getElementById(inputId);
  const icon = btn.querySelector('i');
  if (input.type === 'password') {
    input.type = 'text';
    icon.className = 'fa fa-eye-slash';
  } else {
    input.type = 'password';
    icon.className = 'fa fa-eye';
  }
}
