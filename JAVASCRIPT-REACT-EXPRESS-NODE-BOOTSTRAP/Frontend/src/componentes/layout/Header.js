import React from "react";
import '../../styles/componentes/layout/bootstrap.css';

const Header=(props)=>{
    return(
        <header>
            <div className="holder">
                <div className="logo">
                    <center>
                        <img src="/tree.jpg" width="300" alt=""/>
                    </center>
                </div>
                <br></br>
                <div>
                    <center>
                        <img src="/librosonline.jpg" width="300" alt=""/>
                    </center>
                </div>
            </div>
        </header>
    
    );   


}
export default Header;