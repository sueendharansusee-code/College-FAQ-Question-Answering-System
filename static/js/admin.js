/**
 * Admin Portal Management Script
 * College FAQ Question-Answering System
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const totalFaqsCount = document.getElementById('totalFaqsCount');
  const totalQueriesCount = document.getElementById('totalQueriesCount');
  const resolutionRate = document.getElementById('resolutionRate');
  const totalCategoriesCount = document.getElementById('totalCategoriesCount');

  const faqsTableBody = document.getElementById('faqsTableBody');
  const faqSearchInput = document.getElementById('faqSearchInput');
  const faqCategoryFilter = document.getElementById('faqCategoryFilter');
  const openAddFaqModalBtn = document.getElementById('openAddFaqModalBtn');

  const faqModal = document.getElementById('faqModal');
  const faqModalTitle = document.getElementById('faqModalTitle');
  const faqForm = document.getElementById('faqForm');
  const faqIdInput = document.getElementById('faqIdInput');
  const faqCategorySelect = document.getElementById('faqCategorySelect');
  const faqQuestionInput = document.getElementById('faqQuestionInput');
  const faqAnswerInput = document.getElementById('faqAnswerInput');
  const faqKeywordsInput = document.getElementById('faqKeywordsInput');
  const closeModalBtn = document.getElementById('closeModalBtn');
  const cancelFaqBtn = document.getElementById('cancelFaqBtn');

  const historyTableBody = document.getElementById('historyTableBody');
  const historyStatusFilter = document.getElementById('historyStatusFilter');
  const clearHistoryBtn = document.getElementById('clearHistoryBtn');

  const sandboxForm = document.getElementById('sandboxForm');
  const sandboxQueryInput = document.getElementById('sandboxQueryInput');
  const sandboxResults = document.getElementById('sandboxResults');

  // Tab Navigation
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanels = document.querySelectorAll('.tab-panel');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      tabPanels.forEach(p => p.style.display = 'none');

      btn.classList.add('active');
      const targetPanel = document.getElementById(btn.getAttribute('data-target'));
      if (targetPanel) targetPanel.style.display = 'block';
    });
  });

  // Global Categories Cache
  let categoriesMap = {};

  // Initial Load
  loadAnalytics();
  loadCategoriesDropdown();
  loadFaqsTable();
  loadQueryHistory();

  // Search & Category Filter Listeners
  if (faqSearchInput) {
    faqSearchInput.addEventListener('input', debounce(() => loadFaqsTable(), 300));
  }
  if (faqCategoryFilter) {
    faqCategoryFilter.addEventListener('change', () => loadFaqsTable());
  }

  // History Filter
  if (historyStatusFilter) {
    historyStatusFilter.addEventListener('change', () => loadQueryHistory());
  }

  // Clear History Event
  if (clearHistoryBtn) {
    clearHistoryBtn.addEventListener('click', async () => {
      if (confirm('Are you sure you want to clear all query history logs?')) {
        await fetch('/api/admin/history', { method: 'DELETE' });
        loadQueryHistory();
        loadAnalytics();
      }
    });
  }

  // Add FAQ Modal Trigger
  if (openAddFaqModalBtn) {
    openAddFaqModalBtn.addEventListener('click', () => {
      faqModalTitle.innerText = 'Add New FAQ';
      faqIdInput.value = '';
      faqForm.reset();
      openModal();
    });
  }

  // Close Modal Events
  if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);
  if (cancelFaqBtn) cancelFaqBtn.addEventListener('click', closeModal);

  // Form Submit (Add/Edit FAQ)
  if (faqForm) {
    faqForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const faqId = faqIdInput.value;
      const categoryId = parseInt(faqCategorySelect.value);
      const question = faqQuestionInput.value.trim();
      const answer = faqAnswerInput.value.trim();
      const keywords = faqKeywordsInput.value.trim();

      if (!categoryId || !question || !answer) {
        alert('Please fill in Category, Question, and Answer.');
        return;
      }

      const payload = { category_id: categoryId, question, answer, keywords };
      const url = faqId ? `/api/admin/faq/${faqId}` : '/api/admin/faq';
      const method = faqId ? 'PUT' : 'POST';

      try {
        const response = await fetch(url, {
          method,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const result = await response.json();
        if (result.success) {
          closeModal();
          loadFaqsTable();
          loadAnalytics();
          alert(faqId ? 'FAQ updated successfully!' : 'FAQ created successfully!');
        } else {
          alert('Error: ' + result.message);
        }
      } catch (err) {
        console.error('Error saving FAQ:', err);
        alert('Server error saving FAQ.');
      }
    });
  }

  // Sandbox Form Submit
  if (sandboxForm) {
    sandboxForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const query = sandboxQueryInput.value.trim();
      if (!query) return;

      sandboxResults.innerHTML = '<div style="padding:1rem; text-align:center;"><i class="fa-solid fa-spinner fa-spin"></i> Running Cosine Similarity Vectorization...</div>';

      try {
        const response = await fetch('/api/admin/test-similarity', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query })
        });
        const data = await response.json();

        if (data.success && data.results) {
          let html = `
            <p style="margin-bottom:0.75rem; font-size:0.9rem;">
              <strong>Preprocessed Tokens:</strong> <code>${escapeHtml(data.processed_tokens || 'None')}</code>
            </p>
            <table class="data-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Category</th>
                  <th>Question</th>
                  <th>Similarity Score</th>
                  <th>Confidence Match</th>
                </tr>
              </thead>
              <tbody>
          `;

          data.results.forEach((item, index) => {
            const scoreNum = parseFloat(item.similarity_score);
            let badgeClass = 'confidence-unreliable';
            if (scoreNum >= 0.70) badgeClass = 'confidence-high';
            else if (scoreNum >= 0.40) badgeClass = 'confidence-medium';
            else if (scoreNum >= 0.20) badgeClass = 'confidence-low';

            html += `
              <tr>
                <td><strong>#${index + 1}</strong></td>
                <td><span class="category-tag">${escapeHtml(item.category)}</span></td>
                <td>${escapeHtml(item.question)}</td>
                <td><strong>${item.score_percentage}</strong> (${item.similarity_score})</td>
                <td><span class="confidence-badge ${badgeClass}">${scoreNum >= 0.20 ? 'Match' : 'Below Threshold'}</span></td>
              </tr>
            `;
          });

          html += `</tbody></table>`;
          sandboxResults.innerHTML = html;
        } else {
          sandboxResults.innerHTML = '<p style="color:var(--danger)">Error testing similarity.</p>';
        }
      } catch (err) {
        console.error('Error testing similarity:', err);
        sandboxResults.innerHTML = '<p style="color:var(--danger)">Server error in sandbox.</p>';
      }
    });
  }

  // Analytics Loader
  async function loadAnalytics() {
    try {
      const response = await fetch('/api/admin/analytics');
      const data = await response.json();
      if (data.success) {
        const a = data.analytics;
        if (totalFaqsCount) totalFaqsCount.innerText = a.total_faqs;
        if (totalQueriesCount) totalQueriesCount.innerText = a.total_queries;
        if (resolutionRate) resolutionRate.innerText = `${a.resolution_rate}%`;
        if (totalCategoriesCount) totalCategoriesCount.innerText = a.total_categories;
      }
    } catch (err) {
      console.error('Error loading analytics:', err);
    }
  }

  // Categories Dropdown Loader
  async function loadCategoriesDropdown() {
    try {
      const response = await fetch('/api/categories');
      const data = await response.json();

      if (data.success) {
        if (faqCategoryFilter) {
          faqCategoryFilter.innerHTML = '<option value="">All Categories</option>';
        }
        if (faqCategorySelect) {
          faqCategorySelect.innerHTML = '<option value="">Select Category...</option>';
        }

        data.categories.forEach(cat => {
          categoriesMap[cat.id] = cat.name;
          if (faqCategoryFilter) {
            faqCategoryFilter.innerHTML += `<option value="${cat.id}">${cat.name}</option>`;
          }
          if (faqCategorySelect) {
            faqCategorySelect.innerHTML += `<option value="${cat.id}">${cat.name}</option>`;
          }
        });
      }
    } catch (err) {
      console.error('Error loading categories dropdown:', err);
    }
  }

  // Load FAQs Table
  async function loadFaqsTable() {
    try {
      const catId = faqCategoryFilter ? faqCategoryFilter.value : '';
      const search = faqSearchInput ? faqSearchInput.value : '';

      let url = `/api/faqs?`;
      if (catId) url += `category_id=${catId}&`;
      if (search) url += `search=${encodeURIComponent(search)}&`;

      const response = await fetch(url);
      const data = await response.json();

      if (data.success && faqsTableBody) {
        faqsTableBody.innerHTML = '';
        if (data.faqs.length === 0) {
          faqsTableBody.innerHTML = `<tr><td colspan="5" style="text-align:center; color:var(--text-muted);">No FAQs found.</td></tr>`;
          return;
        }

        data.faqs.forEach(faq => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td><strong>#${faq.id}</strong></td>
            <td><span class="category-tag"><i class="fa-solid ${faq.category_icon || 'fa-folder'}"></i> ${escapeHtml(faq.category_name)}</span></td>
            <td><strong>${escapeHtml(faq.question)}</strong></td>
            <td><span style="font-size:0.85rem; color:var(--text-muted);">${escapeHtml(faq.answer.substring(0, 80))}${faq.answer.length > 80 ? '...' : ''}</span></td>
            <td>
              <div class="action-btns">
                <button class="action-btn edit" onclick="editFaq(${faq.id})"><i class="fa-solid fa-pen"></i></button>
                <button class="action-btn delete" onclick="deleteFaq(${faq.id})"><i class="fa-solid fa-trash"></i></button>
              </div>
            </td>
          `;
          faqsTableBody.appendChild(tr);
        });
      }
    } catch (err) {
      console.error('Error loading FAQs table:', err);
    }
  }

  // Load Query History Table
  async function loadQueryHistory() {
    try {
      const status = historyStatusFilter ? historyStatusFilter.value : '';
      let url = `/api/admin/history?`;
      if (status) url += `status=${status}&`;

      const response = await fetch(url);
      const data = await response.json();

      if (data.success && historyTableBody) {
        historyTableBody.innerHTML = '';
        if (data.history.length === 0) {
          historyTableBody.innerHTML = `<tr><td colspan="6" style="text-align:center; color:var(--text-muted);">No query logs recorded yet.</td></tr>`;
          return;
        }

        data.history.forEach(log => {
          const isAnswered = log.status === 'ANSWERED';
          const badgeClass = isAnswered ? 'confidence-high' : 'confidence-unreliable';
          const scorePercent = `${roundNum(log.similarity_score * 100, 1)}%`;

          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${log.id}</td>
            <td><strong>${escapeHtml(log.user_query)}</strong></td>
            <td>${escapeHtml(log.matched_question || 'None')}</td>
            <td><span class="confidence-badge ${badgeClass}">${scorePercent}</span></td>
            <td><span class="category-tag">${log.category_name || 'N/A'}</span></td>
            <td><span style="font-size:0.8rem; color:var(--text-muted);">${log.timestamp}</span></td>
          `;
          historyTableBody.appendChild(tr);
        });
      }
    } catch (err) {
      console.error('Error loading query history:', err);
    }
  }

  // Edit FAQ Callback
  window.editFaq = async function(id) {
    try {
      const response = await fetch(`/api/faqs`);
      const data = await response.json();
      const faq = data.faqs.find(f => f.id === id);

      if (faq) {
        faqModalTitle.innerText = 'Edit FAQ #' + id;
        faqIdInput.value = faq.id;
        faqCategorySelect.value = faq.category_id;
        faqQuestionInput.value = faq.question;
        faqAnswerInput.value = faq.answer;
        faqKeywordsInput.value = faq.keywords || '';
        openModal();
      }
    } catch (err) {
      console.error('Error fetching FAQ details for edit:', err);
    }
  };

  // Delete FAQ Callback
  window.deleteFaq = async function(id) {
    if (confirm(`Are you sure you want to delete FAQ #${id}?`)) {
      try {
        const response = await fetch(`/api/admin/faq/${id}`, { method: 'DELETE' });
        const result = await response.json();
        if (result.success) {
          loadFaqsTable();
          loadAnalytics();
        } else {
          alert('Error: ' + result.message);
        }
      } catch (err) {
        console.error('Error deleting FAQ:', err);
      }
    }
  };

  function openModal() {
    if (faqModal) faqModal.classList.add('active');
  }

  function closeModal() {
    if (faqModal) faqModal.classList.remove('active');
  }

  function roundNum(val, dec) {
    return Number(Math.round(val + 'e' + dec) + 'e-' + dec);
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }
});
