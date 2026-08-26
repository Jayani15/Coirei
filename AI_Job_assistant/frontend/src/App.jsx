import { useState } from "react";
import Chat from "../Chat";
import Login from "../Login";

function App() {

  const [loggedIn, setLoggedIn] = useState(
    !!localStorage.getItem("user_id")
  );

  const handleLogin = () => {
    setLoggedIn(true);
  };

  if (!loggedIn) {
    return <Login onLogin={handleLogin} />;
  }

  return <Chat />;
}

export default App;