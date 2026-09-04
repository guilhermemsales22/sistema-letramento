import React, { useState } from 'react';
import Login from './Login';
import HistoricoAluno from './HistoricoAluno';

function App() {
  const [usuarioLogado, setUsuarioLogado] = useState(null);

  // Se o usuário NÃO estiver logado, exibe a tela de login
  if (!usuarioLogado) {
    return <Login aoLogar={setUsuarioLogado} />;
  }

  // Se estiver logado, exibe o painel do sistema com a opção de sair
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <header className="max-w-4xl mx-auto flex justify-between items-center mb-6 bg-white p-4 rounded shadow">
        <h1 className="text-xl font-bold text-gray-700">Bem-vindo(a), {usuarioLogado.nome}</h1>
        <button 
          onClick={() => setUsuarioLogado(null)}
          className="bg-red-500 text-white px-4 py-2 rounded text-sm hover:bg-red-600"
        >
          Sair
        </button>
      </header>
      
      {/* Exibe o histórico do aluno com ID 1 */}
      <HistoricoAluno alunoId={1} />
    </div>
  );
}

export default App;