import React, { useState, useEffect } from 'react';

function LoginButton({ isLoggedIn, setIsLoggedIn, setShow, onLogout } ) {

  const [clientId, setClientId] = useState('');
    
    useEffect(() => {
    // Fetch the client_id 
    fetch('/api/get-client-id')
      .then(response => response.json())
      .then(data => {
        setClientId(data.client_id);
        //console.error("I was here", response)
      })
      .catch(error => {
        //console.error("Failed to fetch client_id:", error);
      });
  }, []);
 
  const handleClick = () => {
    
    const scopes = [
      'url:GET|/api/v1/courses',
      'url:GET|/api/v1/users/:user_id/courses', 
      'url:GET|/api/v1/courses/:course_id/groups', 
      'url:GET|/api/v1/courses/:course_id/settings',
      'url:GET|/api/v1/group_categories/:group_category_id',
      'url:GET|/api/v1/courses/:course_id/search_users',
      'url:GET|/api/v1/groups/:group_id',
      'url:GET|/api/v1/courses/:course_id/group_categories',
      'url:GET|/api/v1/group_categories/:group_category_id/groups',
  ]

    const redirect_uri =  window.location.origin; // must be "https://localhost:3000", will crash on http
    const scopeParam = scopes.join(' '); // Must have a single space,' ' 
    const client_id = clientId;
    const response_type = 'code';
    const state = 'YYY';
    const authUrl = `https://canvas.uw.edu/login/oauth2/auth?client_id=${client_id}&response_type=${response_type}&redirect_uri=${redirect_uri}&state=${state}&scope=${scopeParam}`;
    window.location.href = authUrl;
  };

  useEffect(() => {
    
    const handleAuthCallback = () => {
      const searchParams = new URLSearchParams(window.location.search);
      const code = searchParams.get('code');
      if(code){
        fetch('/api/authorization-code', {
          method: 'POST',
          body: JSON.stringify({ code: code, currentUrl: window.location.origin }),
          headers: { 'Content-Type': 'application/json' },
        })
          .then(response => {
            if (response.status === 200) {
              setIsLoggedIn(true);
            }
          })
          .catch(error => {
            console.log(error)
          });
      }
      else{ // Check login status
        fetch('/api/check-login')
        .then(response => 
          response.json()
        )
        .then(data => {          
          setIsLoggedIn(data.isLoggedIn);
        })
        .catch(error => {
          console.log(error);
          setIsLoggedIn(false);
        });
      }
    
    };
    
    window.addEventListener('load', handleAuthCallback);
    return () => {
      window.removeEventListener('load', handleAuthCallback);
    };
  }, []);

  function handleLogout() {

    setIsLoggedIn(false);
    
    if (onLogout) { 
      onLogout();  // Close the drawer when logging out in the Dashboard
   } 

    sessionStorage.removeItem('authorizationCode');
    fetch('/api/access_token', {
      method: 'DELETE',
    })
      .catch(error => {
        console.log(error)
      });
  }

  const style = {
    background: '#4CAF50',
    border: 'none',
    color: 'white',
    padding: '20px 20px',
    textAlign: 'center',
    textDecoration: 'none',
    fontSize: '16px',
    width: '200px',  // set fixed width
    height: '57px', // set fixed height
    display: 'flex', // these three lines help center the content
    justifyContent: 'center',
    alignItems: 'center',
  }

  return (
    <div>
      {isLoggedIn ? (
        <button style={style} onClick={handleLogout}>Logout</button>
      ) : (
        <button style={style} onClick={handleClick}>Login with Canvas</button>
    )}
    </div>
  );
}

export default LoginButton;