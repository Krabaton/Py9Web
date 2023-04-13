token = localStorage.getItem('accessToken')

const get_cats = async () => {
  const response = await fetch('http://localhost:8000/api/cats', {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  console.log(response.status, response.statusText)
  if (response.status === 200) {
    result = await response.json()
    for (cat of result) {
      el = document.createElement('li')
      el.className = 'list-group-item'
      el.innerHTML = `ID: ${cat.id} name: <b>${cat.nickname}</b> Status: ${cat.vaccinated} Owner: ${cat.owner.email}`
      cats.appendChild(el)
    }
  }
}

const get_owners = async () => {
  const response = await fetch('http://localhost:8000/api/owners', {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  console.log(response.status, response.statusText)
  if (response.status === 200) {
    result = await response.json()
    owners.innerHTML = ''
    for (owner of result) {
      el = document.createElement('li')
      el.className = 'list-group-item'
      el.innerHTML = `ID: ${owner.id} email: ${owner.email}`
      owners.appendChild(el)
    }
  }
}

get_cats()
get_owners()

ownerCreate.addEventListener('submit', async (e) => {
  e.preventDefault()
  const response = await fetch('http://localhost:8000/api/owners', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      email: ownerCreate.email.value,
    }),
  })
  if (response.status === 201) {
    console.log('Ви успішно створили власника')
    get_owners()
  }
})
