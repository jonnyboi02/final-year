const apiUrl = 'http://localhost:8000'; // replace this with your API's URL

export function login(username, password) {
  return fetch(`${apiUrl}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, password })
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(response.statusText);
      }
      return response.json();
    })
    .then(data => {
      const { token } = data;
      localStorage.setItem('token', token); // store the token in localStorage
      return data;
    });
}

export function logout() {
    localStorage.removeItem('token'); // remove the token from localStorage
  }
  
  export function getAuthorizationHeader() {
    const token = localStorage.getItem('token');
    if (token) {
      return { Authorization: `Bearer ${token}` };
    } else {
      return {};
    }
  }