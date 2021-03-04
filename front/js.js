console.log('sanity check')

fetch('http://localhost:8000/api/products/1')
  .then(res => res.json())
  .then(data => console.log(data))
