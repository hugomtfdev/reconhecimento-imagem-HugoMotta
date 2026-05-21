/**
 * TaskFlow — app.js
 * Vanilla JS | localStorage persistence
 * DB shape: { users: [], todos: [] }
 */

// ─── DB layer ──────────────────────────────────────────────────────────────
const DB = {
  get users() { return JSON.parse(localStorage.getItem('users') || '[]'); },
  get todos()  { return JSON.parse(localStorage.getItem('todos')  || '[]'); },

  saveUsers(data) { localStorage.setItem('users', JSON.stringify(data)); },
  saveTodos(data) { localStorage.setItem('todos', JSON.stringify(data)); },

  findUser(email) { return this.users.find(u => u.email === email) ?? null; },
  addUser(user)   { const u = this.users; u.push(user); this.saveUsers(u); },

  /** Returns todos for a user, sorted pending-first, optionally filtered. */
  getUserTodos(userId, filter = 'all') {
    const all = this.todos.filter(t => t.userId === userId);
    const sorted = [...all].sort((a, b) => Number(a.done) - Number(b.done));
    if (filter === 'pending') return sorted.filter(t => !t.done);
    if (filter === 'done')    return sorted.filter(t =>  t.done);
    return sorted;
  },

  addTodo(todo)    { const t = this.todos; t.push(todo); this.saveTodos(t); },
  completeTodo(id) { this.saveTodos(this.todos.map(t => t.id === id ? { ...t, done: true } : t)); },
  deleteTodo(id)   { this.saveTodos(this.todos.filter(t => t.id !== id)); },
};

// ─── State ─────────────────────────────────────────────────────────────────
let currentFilter = 'all';

// ─── Helpers ───────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);

const escapeHtml = str =>
  String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');

const isValidEmail = email => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

// ─── View router ───────────────────────────────────────────────────────────
const VIEWS = ['login-view', 'register-view', 'dashboard-view'];

function showView(name) {
  VIEWS.forEach(id => {
    $(id).classList.toggle('hidden-view', id !== name);
  });
}

// ─── Inline error helpers ──────────────────────────────────────────────────
function showError(id, msg) {
  const el = $(id);
  if (!el) return;
  el.textContent = msg;
  el.classList.remove('hidden-view');
}

function hideEl(id) {
  const el = $(id);
  if (!el) return;
  el.textContent = '';
  el.classList.add('hidden-view');
}

function clearErrors(...ids) { ids.forEach(hideEl); }

// ─── Session ───────────────────────────────────────────────────────────────
function getCurrentUser() {
  const raw = localStorage.getItem('currentUser');
  return raw ? JSON.parse(raw) : null;
}

function saveSession(user) {
  localStorage.setItem('currentUser', JSON.stringify({ name: user.name, email: user.email }));
}

function clearSession() {
  localStorage.removeItem('currentUser');
}

// ─── Auth handlers ─────────────────────────────────────────────────────────
function handleRegister(e) {
  e.preventDefault();
  clearErrors(
    'register-name-error', 'register-email-error',
    'register-password-error', 'register-general-error', 'register-success'
  );

  const name     = $('register-name').value.trim();
  const email    = $('register-email').value.trim();
  const password = $('register-password').value;
  let ok = true;

  if (!name)                       { showError('register-name-error',     'Nome é obrigatório.');           ok = false; }
  if (!email)                      { showError('register-email-error',    'E-mail é obrigatório.');          ok = false; }
  else if (!isValidEmail(email))   { showError('register-email-error',    'Informe um e-mail válido.');      ok = false; }
  if (!password)                   { showError('register-password-error', 'Senha é obrigatória.');           ok = false; }
  else if (password.length < 6)   { showError('register-password-error', 'Mínimo de 6 caracteres.');  ok = false; }

  if (!ok) return;

  if (DB.findUser(email)) {
    showError('register-general-error', 'Este e-mail já está em uso.');
    return;
  }

  DB.addUser({ name, email, password });

  const successEl = $('register-success');
  successEl.textContent = '✓ Conta criada com sucesso! Redirecionando…';
  successEl.classList.remove('hidden-view');

  $('register-form').reset();

  setTimeout(() => {
    hideEl('register-success');
    showView('login-view');
  }, 1600);
}

function handleLogin(e) {
  e.preventDefault();
  clearErrors('login-email-error', 'login-password-error', 'login-general-error');

  const email    = $('login-email').value.trim();
  const password = $('login-password').value;
  let ok = true;

  if (!email)                    { showError('login-email-error',    'E-mail é obrigatório.');    ok = false; }
  else if (!isValidEmail(email)) { showError('login-email-error',    'E-mail inválido.');          ok = false; }
  if (!password)                 { showError('login-password-error', 'Senha é obrigatória.');      ok = false; }

  if (!ok) return;

  const user = DB.findUser(email);
  if (!user)                        { showError('login-general-error', 'E-mail não cadastrado.'); return; }
  if (user.password !== password)   { showError('login-general-error', 'Senha incorreta.');        return; }

  saveSession(user);
  $('login-form').reset();
  enterDashboard(user);
}

// ─── Dashboard ─────────────────────────────────────────────────────────────
function enterDashboard(user) {
  showView('dashboard-view');
  $('user-name-display').textContent = user.name;
  $('user-avatar').textContent = user.name.charAt(0).toUpperCase();
  setFilter('all');
}

function setFilter(filter) {
  currentFilter = filter;
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.filter === filter);
  });
  renderTasks(getCurrentUser().email);
}

// ─── Badge map ─────────────────────────────────────────────────────────────
const BADGE = {
  Trabalho: { cls: 'badge--trabalho', icon: '💼' },
  Pessoal:  { cls: 'badge--pessoal',  icon: '🙂' },
  Estudos:  { cls: 'badge--estudos',  icon: '📚' },
};

// ─── Task renderer ─────────────────────────────────────────────────────────
function renderTasks(userId) {
  const tasks    = DB.getUserTodos(userId, currentFilter);
  const allTasks = DB.getUserTodos(userId, 'all');

  // Update stats (always from full list)
  $('stat-total').textContent   = allTasks.length;
  $('stat-pending').textContent = allTasks.filter(t => !t.done).length;
  $('stat-done').textContent    = allTasks.filter(t =>  t.done).length;

  const list = $('task-list');
  list.innerHTML = '';

  const isEmpty = tasks.length === 0;
  $('empty-state').classList.toggle('hidden-view', !isEmpty);

  if (isEmpty) return;

  tasks.forEach(task => {
    const { cls: badgeCls, icon } = BADGE[task.type] ?? BADGE.Trabalho;
    const card = document.createElement('div');
    card.className = `task-card${task.done ? ' done' : ''}`;
    card.dataset.id = task.id;

    card.innerHTML = `
      <div class="task-card-inner">
        <div class="task-meta">
          <div class="task-header">
            <span class="task-title">${escapeHtml(task.title)}</span>
            <span class="badge ${badgeCls}">${icon} ${task.type}</span>
            ${task.done ? '<span class="badge badge--done">✓ Concluída</span>' : ''}
          </div>
          ${task.description
            ? `<p class="task-description">${escapeHtml(task.description)}</p>`
            : ''}
        </div>
        <div class="task-actions">
          ${!task.done
            ? `<button class="btn-complete" data-id="${task.id}" aria-label="Concluir tarefa">✓ Concluir</button>`
            : `<button class="btn-complete done" disabled aria-label="Tarefa concluída">✓ Feito</button>`}
          <button class="btn-delete" data-id="${task.id}" aria-label="Excluir tarefa">✕</button>
        </div>
      </div>
    `;

    list.appendChild(card);
  });

  // Delegate events
  list.querySelectorAll('.btn-complete:not(.done)').forEach(btn => {
    btn.addEventListener('click', () => {
      DB.completeTodo(btn.dataset.id);
      renderTasks(getCurrentUser().email);
    });
  });

  list.querySelectorAll('.btn-delete').forEach(btn => {
    btn.addEventListener('click', () => {
      DB.deleteTodo(btn.dataset.id);
      renderTasks(getCurrentUser().email);
    });
  });
}

// ─── Task form handler ─────────────────────────────────────────────────────
function handleAddTask(e) {
  e.preventDefault();
  hideEl('task-title-error');

  const title       = $('task-title').value.trim();
  const type        = $('task-type').value;
  const description = $('task-description').value.trim();

  if (!title) {
    showError('task-title-error', 'O título é obrigatório.');
    return;
  }

  const user = getCurrentUser();
  DB.addTodo({
    id:          String(Date.now()),
    userId:      user.email,
    title,
    type,
    description,
    done:        false,
    createdAt:   new Date().toISOString(),
  });

  $('task-form').reset();
  renderTasks(user.email);
}

// ─── Init ──────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {

  // Navigation links
  $('go-to-register').addEventListener('click', e => {
    e.preventDefault();
    clearErrors('login-email-error', 'login-password-error', 'login-general-error');
    $('login-form').reset();
    showView('register-view');
  });

  $('go-to-login').addEventListener('click', e => {
    e.preventDefault();
    clearErrors(
      'register-name-error', 'register-email-error',
      'register-password-error', 'register-general-error', 'register-success'
    );
    $('register-form').reset();
    showView('login-view');
  });

  // Auth forms
  $('register-form').addEventListener('submit', handleRegister);
  $('login-form').addEventListener('submit', handleLogin);

  // Logout
  $('logout-btn').addEventListener('click', () => {
    clearSession();
    currentFilter = 'all';
    showView('login-view');
  });

  // Task form
  $('task-form').addEventListener('submit', handleAddTask);

  // Filter buttons
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => setFilter(btn.dataset.filter));
  });

  // Bootstrap: restore session
  const user = getCurrentUser();
  if (user) {
    enterDashboard(user);
  } else {
    showView('login-view');
  }
});
