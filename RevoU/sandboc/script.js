const data = [
    {
        deskripsi: "Hoodie ini memiliki bahan dengan kualitas terbaik...",
        harga: 250000,
        id: 1,
        image: "hero.jpeg",
        nama: "Hoodie SPH",
        status: "Publish",
        stock: 0
    },
    {
        deskripsi: "Keychain dengan desain logo SPH...",
        harga: 15000,
        id: 2,
        image: "hero.png",
        nama: "Keychain SPH",
        status: "Publish",
        stock: 0
    },
    {
        deskripsi: "Sticker karakter SPH lucu...",
        harga: 2000,
        id: 3,
        image: "hero.png",
        nama: "Sticker SPH",
        status: "Unpublish",
        stock: 0
    },
    {
        deskripsi: "Totebag kain tebal dengan sablon logo SPH...",
        harga: 85000,
        id: 4,
        image: "hero.png",
        nama: "Totebag SPH",
        status: "Publish",
        stock: 0
    }
];

const productList = document.getElementById('productList');
const sideForm = document.getElementById('sideForm');
const addProductBtn = document.getElementById('addProductBtn');

function formatRupiah(angka) {
  return "Rp" + angka.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function renderProducts() {
  productList.innerHTML = '';
  data.forEach((item) => {
    const div = document.createElement('div');
    div.className = 'product-item';

    div.innerHTML = `
      <div class="product-info">
        <img src="${item.image}" alt="${item.nama}">
        <div>
          <strong>${item.nama}</strong>
          <p>${item.deskripsi.slice(0, 50)}...</p>
          <p>${formatRupiah(item.harga)}</p>
        </div>
      </div>
      <div class="actions">
        <button class="action-button" onclick="toggleDropdown(${item.id})">⋮</button>
        <div class="dropdown" id="dropdown-${item.id}">
          <button onclick="editProduct(${item.id})">Edit</button>
          <button class="delete" onclick="deleteProduct(${item.id})">Delete</button>
        </div>
      </div>
    `;
    productList.appendChild(div);
  });
}

function toggleDropdown(id) {
  document.querySelectorAll('.dropdown').forEach(drop => drop.classList.remove('show'));
  const dropdown = document.getElementById(`dropdown-${id}`);
  if (dropdown) {
    dropdown.classList.toggle('show');
  }
}

function editProduct(id) {
  console.log("Edit Product ID:", id);
  sideForm.classList.add('show');
}

function deleteProduct(id) {
  console.log("Delete Product ID:", id);
  sideForm.classList.add('show');
}

addProductBtn.addEventListener('click', () => {
  sideForm.classList.add('show');
});

// Close dropdowns if clicking outside
document.addEventListener('click', (e) => {
  if (!e.target.closest('.actions')) {
    document.querySelectorAll('.dropdown').forEach(drop => drop.classList.remove('show'));
  }
});

renderProducts();
