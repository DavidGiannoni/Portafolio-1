import './App.css';
import { BrowserRouter as Router,Switch ,Route } from "react-router-dom";
import Header from './componentes/layout/Header';
import Footer from './componentes/layout/Footer';
import Nav from './componentes/layout/Nav';
import HomePage from './pages/HomePage';
import NosotrosPage from './pages/NosotrosPage';
import ContactoPage from './pages/ContactoPage';
import NovedadesPage from './pages/NovedadesPage';
import Login from './pages/Login';

function App() {
  return (
    
    <div className="App">
      <Router>
      <Header/>
      <Nav/>
      <Switch>
        <Route path= "/" exact component={Login}/>
        <Route path= "/" exact component={HomePage}/>
        <Route path= "/nosotros" exact component={NosotrosPage}/>
        <Route path= "/novedades" exact component={NovedadesPage}/>
        <Route path= "/contacto" exact component={ContactoPage}/>
      </Switch>
      <Footer></Footer>
      </Router>
    </div>
  );
}

export default App;
