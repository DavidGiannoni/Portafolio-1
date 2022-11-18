import React from "react";
import '../../styles/componentes/layout/Nav.css';
import { NavLink } from "react-router-dom";

const Nav=(props)=>{
    return(
        
        <nav>
            <div className="holder">
                <ul>
                <li><NavLink activeClassName="activo" exact to= "/Login">Login</NavLink></li>    
                <li><NavLink activeClassName="activo" exact to= "/">Home</NavLink></li>
                <li><NavLink activeClassName="activo" exact to=  "/nosotros">Nosotros</NavLink></li>
                <li><NavLink activeClassName="activo" exact to= "/novedades">Novedades</NavLink></li>
                <li><NavLink activeClassName="activo" exact to= "/contacto">Contacto</NavLink></li>
                </ul>
            </div>
        </nav>    
    );


}
export default Nav;