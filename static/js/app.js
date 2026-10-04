/**
 * Student Chat Interface Logic
 * College FAQ Question-Answering System
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const chatMessages = document.getElementById('chatMessages');
  const chatForm = document.getElementById('chatForm');
  const userQueryInput = document.getElementById('userQueryInput');
  const categoryPills = document.getElementById('categoryPills');
  const suggestionsChips = document.getElementById('suggestionsChips');
  const themeToggle = document.getElementById('themeToggle');
  const clearChatBtn = document.getElementById('clearChatBtn');

  // Initial State
  let activeCategoryId = null;

  // Initialize Theme
  const savedTheme = localStorage.getItem('college_faq_theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeButtonIcon(savedTheme);

  // Theme Switcher Event
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('college_faq_theme', newTheme);
      updateThemeButtonIcon(newTheme);
    });
  }

  function updateThemeButtonIcon(theme) {
    if (!themeToggle) return;
    themeToggle.innerHTML = theme === 'dark' 
      ? '<i class="fa-solid fa-sun"></i> Light Mode' 
      : '<i class="fa-solid fa-moon"></i> Dark Mode';
  }

  // Load Categories & Suggestions on Start
  loadCategories();
  loadSuggestedQuestions();

  // Handle Form Submit
  if (chatForm) {
    chatForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const question = userQueryInput.value.strip ? userQueryInput.value.strip() : userQueryInput.value.trim();
      if (!question) return;
      
      sendQuestion(question);
      userQueryInput.value = '';
    });
  }

  // Clear Chat Event
  if (clearChatBtn) {
    clearChatBtn.addEventListener('click', () => {
      chatMessages.innerHTML = `
        <div class="message-group bot-group">
          <div class="avatar bot-avatar"><i class="fa-solid fa-robot"></i></div>
          <div class="message-content">
            <div class="message-bubble">
              Hello! I am your <strong>College FAQ Assistant</strong>. Ask me anything about Admissions, Examination, Fees, Hostel, Library, Placements, and Campus facilities!
            </div>
            <div class="message-meta">
              <span class="status-badge"><span class="status-dot"></span> Online</span>
            </div>
          </div>
        </div>
      `;
    });
  }

  // Load Category Pills
  async function loadCategories() {
    try {
      const response = await fetch('/api/categories');
      const data = await response.json();

      if (data.success && categoryPills) {
        categoryPills.innerHTML = `<button class="category-pill active" data-id="all"><i class="fa-solid fa-layer-group"></i> All Categories</button>`;
        
        data.categories.forEach(cat => {
          categoryPills.innerHTML += `
            <button class="category-pill" data-id="${cat.id}">
              <i class="fa-solid ${cat.icon || 'fa-folder'}"></i> ${cat.name} (${cat.faq_count})
            </button>
          `;
        });

        // Add Pill Click Listeners
        document.querySelectorAll('.category-pill').forEach(pill => {
          pill.addEventListener('click', (e) => {
            document.querySelectorAll('.category-pill').forEach(p => p.classList.remove('active'));
            const clickedBtn = e.currentTarget;
            clickedBtn.classList.add('active');
            
            const catId = clickedBtn.getAttribute('data-id');
            activeCategoryId = catId === 'all' ? null : parseInt(catId);
            loadCategoryFaqs(activeCategoryId);
          });
        });
      }
    } catch (err) {
      console.error('Error loading categories:', err);
    }
  }

  // Load Suggested Questions Chips
  async function loadSuggestedQuestions() {
    try {
      const response = await fetch('/api/suggested-questions');
      const data = await response.json();

      if (data.success && suggestionsChips) {
        suggestionsChips.innerHTML = '';
        data.suggestions.forEach(q => {
          const btn = document.createElement('button');
          btn.className = 'chip-btn';
          btn.innerText = q;
          btn.addEventListener('click', () => sendQuestion(q));
          suggestionsChips.appendChild(btn);
        });
      }
    } catch (err) {
      console.error('Error loading suggested questions:', err);
    }
  }

  // Load FAQs when a category pill is selected
  async function loadCategoryFaqs(catId) {
    if (!catId) return;
    try {
      const response = await fetch(`/api/faqs?category_id=${catId}`);
      const data = await response.json();

      if (data.success && data.faqs.length > 0) {
        suggestionsChips.innerHTML = '';
        data.faqs.slice(0, 5).forEach(f => {
          const btn = document.createElement('button');
          btn.className = 'chip-btn';
          btn.innerText = f.question;
          btn.addEventListener('click', () => sendQuestion(f.question));
          suggestionsChips.appendChild(btn);
        });
      }
    } catch (err) {
      console.error('Error filtering FAQs by category:', err);
    }
  }

  // Send Student Question to Flask API
  async function sendQuestion(questionText) {
    // 1. Append User Message
    appendUserMessage(questionText);

    // 2. Append Typing Indicator
    const typingId = appendTypingIndicator();
    scrollToBottom();

    try {
      const response = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: questionText })
      });

      const data = await response.json();

      // Remove typing indicator
      removeTypingIndicator(typingId);

      // 3. Append Bot Response
      appendBotMessage(data, questionText);
      scrollToBottom();
    } catch (err) {
      removeTypingIndicator(typingId);
      appendBotMessage({
        success: false,
        answer: 'Server connection error. Please try again later.',
        confidence_level: 'Unreliable',
        score_percentage: '0.0%',
        status: 'UNANSWERED'
      }, questionText);
      scrollToBottom();
    }
  }

  function appendUserMessage(text) {
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const userHtml = `
      <div class="message-group user-group">
        <div class="avatar user-avatar"><i class="fa-solid fa-user"></i></div>
        <div class="message-content">
          <div class="message-bubble">${escapeHtml(text)}</div>
          <div class="message-meta">${timeStr}</div>
        </div>
      </div>
    `;
    chatMessages.insertAdjacentHTML('beforeend', userHtml);
  }

  function appendBotMessage(data, originalQuery) {
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    // Determine Confidence Class
    let confClass = 'confidence-unreliable';
    let confIcon = 'fa-circle-exclamation';

    if (data.confidence_level === 'High') {
      confClass = 'confidence-high';
      confIcon = 'fa-circle-check';
    } else if (data.confidence_level === 'Medium') {
      confClass = 'confidence-medium';
      confIcon = 'fa-circle-info';
    } else if (data.confidence_level === 'Low') {
      confClass = 'confidence-low';
      confIcon = 'fa-triangle-exclamation';
    }

    // Build suggestions HTML if confidence low/unreliable or suggestions present
    let suggestionsHtml = '';
    if (data.suggestions && data.suggestions.length > 0) {
      suggestionsHtml += `<div class="suggestions-list"><p style="font-size:0.8rem; font-weight:600; color:var(--text-muted);">Related Questions You Might Mean:</p>`;
      data.suggestions.forEach(s => {
        suggestionsHtml += `
          <button class="suggestion-item-btn" onclick="document.getElementById('userQueryInput').value='${escapeHtml(s.question)}'; sendQuestionFromGlobal('${escapeHtml(s.question)}')">
            <span>${escapeHtml(s.question)}</span>
            <span class="category-tag">${s.category} (${s.score_percentage})</span>
          </button>
        `;
      });
      suggestionsHtml += `</div>`;
    }

    const botHtml = `
      <div class="message-group bot-group">
        <div class="avatar bot-avatar"><i class="fa-solid fa-robot"></i></div>
        <div class="message-content">
          <div class="message-bubble">
            <p>${escapeHtml(data.answer)}</p>
            ${suggestionsHtml}
            
            <details class="nlp-details">
              <summary><i class="fa-solid fa-brain"></i> Similarity Breakdown</summary>
              <div class="nlp-details-content">
                <p><strong>Original Query:</strong> ${escapeHtml(originalQuery)}</p>
                <p><strong>NLTK Tokens:</strong> ${escapeHtml(data.preprocessed_tokens || 'None')}</p>
                <p><strong>Matched FAQ Question:</strong> ${escapeHtml(data.matched_question || 'None')}</p>
                <p><strong>Cosine Similarity Score:</strong> ${data.score_percentage || '0.0%'}</p>
              </div>
            </details>
          </div>

          <div class="message-meta">
            <span class="confidence-badge ${confClass}"><i class="fa-solid ${confIcon}"></i> ${data.confidence_level || 'Unreliable'} (${data.score_percentage || '0.0%'})</span>
            ${data.category ? `<span class="category-tag"><i class="fa-solid ${data.category_icon || 'fa-folder'}"></i> ${data.category}</span>` : ''}
            <span>${timeStr}</span>
          </div>
        </div>
      </div>
    `;

    chatMessages.insertAdjacentHTML('beforeend', botHtml);
  }

  function appendTypingIndicator() {
    const id = 'typing_' + Date.now();
    const html = `
      <div class="message-group bot-group" id="${id}">
        <div class="avatar bot-avatar"><i class="fa-solid fa-robot"></i></div>
        <div class="message-content">
          <div class="message-bubble">
            <div class="typing-indicator">
              <div class="typing-dot"></div>
              <div class="typing-dot"></div>
              <div class="typing-dot"></div>
            </div>
          </div>
        </div>
      </div>
    `;
    chatMessages.insertAdjacentHTML('beforeend', html);
    return id;
  }

  function removeTypingIndicator(id) {
    const elem = document.getElementById(id);
    if (elem) elem.remove();
  }

  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
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

  // Expose global click helper for suggestion buttons
  window.sendQuestionFromGlobal = function(qText) {
    sendQuestion(qText);
  };
});
