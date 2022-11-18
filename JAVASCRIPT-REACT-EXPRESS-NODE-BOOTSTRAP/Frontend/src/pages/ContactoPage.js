import React from "react";
import '../styles/componentes/pages/bootstrap.css';

const ContactoPage = (props)=>{
    return(
        <main className="holder">
            <div className="columna contacto">
                <h1>📋 Formulario de Contacto:</h1>
                <form action="" method=""
                className="form-group" >
                    <p>
                        <label>👤 Nombre:</label>
                        <input type="text" name="nombre" className="form-control"/>
                    </p>
                    <p>
                        <label>✉️ E-mail:</label>
                        <input type="text" name="email" className="form-control" />
                    </p>
                    <p>
                        <label>📞 Telefono:</label>
                        <input type="text" name="telefono" className="form-control"/>
                    </p>
                    <p>
                        <label>📄 Mensaje:</label>
                        <br></br>
                        <textarea name="mensaje" className="form-control" ></textarea>
                    </p>
                    <p className="centrar"><input type="submit" value="Enviar" class="btn btn-secondary"/></p>
                </form>    
            </div>
            <br></br>
            <div className="columna datos">
                <h3>📩 Otras formas de contacto...</h3>
                <br></br>
                <p>Facebook: LibrosOnline!Facebook </p>
                <p>Instagram: LibrosOnline!Instagram </p>
                <p>E-mail: LibrosOnline!@gmail.com</p>
                </div>    
        </main>
    
    );
}
export default ContactoPage;