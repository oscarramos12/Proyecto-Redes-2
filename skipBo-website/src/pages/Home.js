import React from "react";
import { Link } from "react-router-dom";
import BannerImage from "../assets/skipBo.jpg";
import "../styles/Home.css";
import game from "../assets/game/Cliente.zip";

function Home() {
  return (
    <div className="home" style={{ backgroundImage: `url(${BannerImage})` }}>
      <div className="headerContainer">
        <a href={game} download>
          <button> DOWNLOAD GAME </button>
        </a>
      </div>
    </div>
  );
}

export default Home;
