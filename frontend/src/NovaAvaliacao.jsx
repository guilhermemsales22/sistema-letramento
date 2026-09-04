import { useState } from 'react';

export default function NovaAvaliacao({ alunoId = 1 }) {
    const [formData, setFormData] = useState({
        aluno_id: alunoId,
        periodo: '1º Bimestre',
        nivel_letramento: 'PS', // Pré-Silábico, Silábico, etc.
        habilidades_adquiridas: '',
        pontos_estimulo: '',
        data_avaliacao: new Date().toISOString().split('T')[0] // Data de hoje no formato YYYY-MM-DD
    });

    const [mensagem, setMensagem] = useState('');

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        try {
            const response = await fetch('http://127.0.0.1:8000/avaliacoes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                setMensagem('Avaliação cadastrada com sucesso!');
                // Limpa os campos de texto após o envio
                setFormData({ ...formData, habilidades_adquiridas: '', pontos_estimulo: '' });
            } else {
                setMensagem('Erro ao cadastrar avaliação. Verifique os dados.');
            }
        } catch (error) {
            console.error("Erro na requisição:", error);
            setMensagem('Erro de conexão com o servidor.');
        }
    };

    return (
        <div style={{ maxWidth: '500px', margin: '20px auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
            <h3>Cadastrar Nova Avaliação</h3>
            
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                
                <label>Período:</label>
                <select name="periodo" value={formData.periodo} onChange={handleChange}>
                    <option value="1º Bimestre">1º Bimestre</option>
                    <option value="2º Bimestre">2º Bimestre</option>
                    <option value="3º Bimestre">3º Bimestre</option>
                    <option value="4º Bimestre">4º Bimestre</option>
                </select>

                <label>Nível de Letramento:</label>
                <select name="nivel_letramento" value={formData.nivel_letramento} onChange={handleChange}>
                    <option value="PS">Pré-Silábico (PS)</option>
                    <option value="SSV">Silábico Sem Valor (SSV)</option>
                    <option value="SCV">Silábico Com Valor (SCV)</option>
                    <option value="SA">Silábico Alfabético (SA)</option>
                    <option value="A">Alfabético (A)</option>
                </select>

                <label>Habilidades Adquiridas:</label>
                <textarea 
                    name="habilidades_adquiridas" 
                    value={formData.habilidades_adquiridas} 
                    onChange={handleChange} 
                    required 
                    rows="3"
                />

                <label>Pontos de Estímulo (Dificuldades):</label>
                <textarea 
                    name="pontos_estimulo" 
                    value={formData.pontos_estimulo} 
                    onChange={handleChange} 
                    required 
                    rows="3"
                />

                <label>Data da Avaliação:</label>
                <input 
                    type="date" 
                    name="data_avaliacao" 
                    value={formData.data_avaliacao} 
                    onChange={handleChange} 
                    required 
                />

                <button type="submit" style={{ padding: '10px', backgroundColor: '#007BFF', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
                    Salvar Avaliação
                </button>
            </form>

            {mensagem && <p style={{ marginTop: '15px', fontWeight: 'bold', color: mensagem.includes('sucesso') ? 'green' : 'red' }}>{mensagem}</p>}
        </div>
    );
}