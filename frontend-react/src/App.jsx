import { useEffect, useState } from 'react';
import './App.css';

function App() {
  const API = 'http://127.0.0.1:5000';

  const [contrasenas, setContrasenas] = useState([]);
  const [plataforma, setPlataforma] = useState('');
  const [usuario, setUsuario] = useState('');
  const [clave, setClave] = useState('');
  const [mensaje, setMensaje] = useState('');
  const [editando, setEditando] = useState(null);

  const obtenerContrasenas = async () => {
    try {
      const respuesta = await fetch(`${API}/baul`);
      if (!respuesta.ok) throw new Error('Error al consultar registros');

      const datos = await respuesta.json();
      setContrasenas(datos);
    } catch (error) {
      setMensaje(error.message);
    }
  };

  useEffect(() => {
    obtenerContrasenas();
  }, []);

  const limpiarFormulario = () => {
    setPlataforma('');
    setUsuario('');
    setClave('');
    setEditando(null);
  };

  const guardarContrasena = async (e) => {
    e.preventDefault();

    const datos = {
      Plataforma: plataforma,
      usuario: usuario,
      clave: clave
    };

    try {
      const respuesta = await fetch(
        editando
          ? `${API}/baul/${editando}`
          : `${API}/baul`,
        {
          method: editando ? 'PUT' : 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(datos)
        }
      );

      const resultado = await respuesta.json();

      if (!respuesta.ok) {
        throw new Error(resultado.mensaje || 'No se pudo guardar');
      }

      setMensaje(resultado.mensaje);
      limpiarFormulario();
      await obtenerContrasenas();

    } catch (error) {
      setMensaje(error.message);
    }
  };

  const prepararEdicion = (registro) => {
    setEditando(registro.id_baul);
    setPlataforma(registro.Plataforma);
    setUsuario(registro.usuario);
    setClave(registro.clave);
    setMensaje('Editando registro seleccionado');
  };

  const eliminarContrasena = async (id) => {
    const confirmar = window.confirm(
      '¿Estás seguro de eliminar este registro?'
    );

    if (!confirmar) return;

    try {
      const respuesta = await fetch(`${API}/baul/${id}`, {
        method: 'DELETE'
      });

      const resultado = await respuesta.json();

      if (!respuesta.ok) {
        throw new Error(resultado.mensaje || 'No se pudo eliminar');
      }

      setMensaje(resultado.mensaje);
      await obtenerContrasenas();

    } catch (error) {
      setMensaje(error.message);
    }
  };

  return (
    <main>
      <h1>Gestor de Contraseñas</h1>

      <h2>{editando ? 'Editar contraseña' : 'Registrar contraseña'}</h2>

      <form onSubmit={guardarContrasena}>
        <input
          type="text"
          placeholder="Plataforma"
          value={plataforma}
          onChange={(e) => setPlataforma(e.target.value)}
          required
        />

        <input
          type="text"
          placeholder="Usuario"
          value={usuario}
          onChange={(e) => setUsuario(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Contraseña"
          value={clave}
          onChange={(e) => setClave(e.target.value)}
          required
        />

        <button type="submit">
          {editando ? 'Actualizar contraseña' : 'Guardar contraseña'}
        </button>

        {editando && (
          <button type="button" onClick={limpiarFormulario}>
            Cancelar edición
          </button>
        )}
      </form>

      <p>{mensaje}</p>

      <h2>Mis contraseñas</h2>

      {contrasenas.length === 0 ? (
        <p>No hay registros disponibles.</p>
      ) : (
        contrasenas.map((registro) => (
          
        <div key={registro.id_baul} className="registro">
          <div className="registro-info">
            <div>
              <h3>{registro.Plataforma}</h3>
              <p>Usuario: {registro.usuario}</p>
              <p>Contraseña: ********</p>
            </div>

            <div className="acciones">
              <button
                type="button"
                onClick={() => prepararEdicion(registro)}
              >
                Editar
              </button>

              <button
                type="button"
                onClick={() => eliminarContrasena(registro.id_baul)}
              >
                Eliminar
              </button>
            </div>
          </div>
        </div>

        ))
      )}
    </main>
  );
}

export default App;