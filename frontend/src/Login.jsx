import React, { useState } from 'react';

export default function Login({ aoLogar }) {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [erro, setErro] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
     const response = await fetch('http://127.0.0.1:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha })
      });
      
      if (!response.ok) throw new Error('E-mail ou senha inválidos');
      
      const data = await response.json();
      aoLogar(data.usuario); // Passa o usuário logado para o App principal
    } catch (err) {
      setErro(err.message);
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <form onSubmit={handleLogin} className="p-8 bg-white rounded-lg shadow-md w-96">
        <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Sistema de Letramento</h2>
        {erro && <div className="mb-4 text-red-500 text-sm">{erro}</div>}
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">E-mail</label>
          <input 
            type="email" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-2 border rounded" 
            required 
          />
        </div>
        <div className="mb-6">
          <label className="block text-gray-700 text-sm font-bold mb-2">Senha</label>
          <input 
            type="password" 
            value={senha} 
            onChange={(e) => setSenha(e.target.value)}
            className="w-full p-2 border rounded" 
            required 
          />
        </div>
        <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded font-bold hover:bg-blue-700">
          Entrar
        </button>
      </form>
    </div>
  );
}