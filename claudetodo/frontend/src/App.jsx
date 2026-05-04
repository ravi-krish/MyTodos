import { useState, useEffect } from 'react';
import { getTodos, createTodo, updateTodo, deleteTodo } from './api';
import './App.css';

function TodoItem({ todo, onToggle, onDelete }) {
  return (
    <li className="todo-item">
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo)}
        className="todo-checkbox"
      />
      <span className={todo.completed ? 'todo-title completed' : 'todo-title'}>
        {todo.title}
      </span>
      <button
        className="delete-btn"
        onClick={() => onDelete(todo.id)}
        aria-label="Delete todo"
      >
        Delete
      </button>
    </li>
  );
}

const FILTERS = ['all', 'pending', 'completed'];

function App() {
  const [todos, setTodos] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [filter, setFilter] = useState('all');

  const refresh = (f = filter) => getTodos(f).then(setTodos);

  useEffect(() => { refresh(filter); }, [filter]);

  const handleAdd = async () => {
    const title = inputValue.trim();
    if (!title) return;
    await createTodo(title);
    setInputValue('');
    refresh();
  };

  const handleToggle = async (todo) => {
    await updateTodo(todo.id, { completed: !todo.completed });
    refresh();
  };

  const handleDelete = async (id) => {
    await deleteTodo(id);
    refresh();
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleAdd();
  };

  return (
    <div className="app">
      <h1>ClaudeTodo</h1>
      <div className="add-row">
        <input
          className="todo-input"
          type="text"
          placeholder="What needs to be done?"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button className="add-btn" onClick={handleAdd}>Add</button>
      </div>
      <div className="filter-tabs">
        {FILTERS.map((f) => (
          <button
            key={f}
            className={`filter-tab${filter === f ? ' active' : ''}`}
            onClick={() => setFilter(f)}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>
      {todos.length === 0 ? (
        <p className="empty-msg">No todos yet. Add one above!</p>
      ) : (
        <ul className="todo-list">
          {todos.map((todo) => (
            <TodoItem
              key={todo.id}
              todo={todo}
              onToggle={handleToggle}
              onDelete={handleDelete}
            />
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
