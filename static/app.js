let hotels=[], currentFilter="all", favorites=JSON.parse(localStorage.getItem("stayqatar-favorites")||"[]");
const $=s=>document.querySelector(s);
const $$=s=>document.querySelectorAll(s);

async function loadHotels(url="/api/hotels"){
  const res=await fetch(url); hotels=await res.json(); render();
}
function render(){
  const list=currentFilter==="all"?hotels:hotels.filter(h=>h.type===currentFilter);
  $("#results").innerHTML=list.map(h=>`
    <article class="card" onclick="openHotel(${h.id})">
      <div class="card-img" style="background-image:url('${h.image}')">
        <button class="heart ${favorites.includes(h.id)?"saved":""}" onclick="event.stopPropagation();toggleFav(${h.id})">${favorites.includes(h.id)?"♥":"♡"}</button>
      </div>
      <div class="card-body"><div class="card-top"><div><h3>${h.name}</h3><div class="location">${h.location}</div></div><div class="rating">★ ${h.rating}</div></div>
      <div class="price"><strong>QAR ${h.price}</strong> / night <span style="float:right" class="type">${h.type}</span></div></div>
    </article>`).join("");
  $("#favCount").textContent=favorites.length;
}
function toggleFav(id){
  favorites=favorites.includes(id)?favorites.filter(x=>x!==id):[...favorites,id];
  localStorage.setItem("stayqatar-favorites",JSON.stringify(favorites));render();toast(favorites.includes(id)?"Saved to favorites":"Removed from favorites");
}
function openHotel(id){
  const h=hotels.find(x=>x.id===id); if(!h)return;
  $("#modalContent").innerHTML=`<img class="detail-img" src="${h.image}" alt="${h.name}">
  <div class="detail-body"><div class="type">${h.type}</div><h2>${h.name}</h2><div class="location">⌖ ${h.location} &nbsp; · &nbsp; ★ ${h.rating}</div>
  <p>${h.desc}</p><div class="detail-grid"><div><b>QAR ${h.price}</b> / night</div><div>Up to <b>${h.guests} guests</b></div></div>
  <h3>Request a booking</h3><form class="book-form" onsubmit="submitBooking(event,${h.id})">
  <input name="name" placeholder="Full name" required><input name="email" type="email" placeholder="Email address" required>
  <input name="checkin" type="date" required><input name="checkout" type="date" required><input name="guests" type="number" min="1" max="${h.guests}" value="2" required>
  <button>Confirm booking request →</button></form></div>`;
  $("#modal").classList.remove("hidden");
}
async function submitBooking(e,id){
  e.preventDefault(); const d=Object.fromEntries(new FormData(e.target).entries());d.hotel_id=id;d.guests=Number(d.guests);
  const res=await fetch("/api/book",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(d)});const out=await res.json();
  if(out.ok){closeModal();toast("Booking confirmed · Reference #"+out.booking_id)}else toast(out.message);
}
function closeModal(){$("#modal").classList.add("hidden")}
function toast(msg){const t=$("#toast");t.textContent=msg;t.classList.add("show");setTimeout(()=>t.classList.remove("show"),2800)}
function openLogin(){toast("Demo mode: booking is available without login.")}
$("#modal").addEventListener("click",e=>{if(e.target.id==="modal")closeModal()});
$("#searchForm").addEventListener("submit",async e=>{e.preventDefault();const q=$("#where").value.trim();await loadHotels(q?"/api/hotels?q="+encodeURIComponent(q):"/api/hotels");$("#stays").scrollIntoView({behavior:"smooth"})});
$$(".filter").forEach(b=>b.addEventListener("click",()=>{$$(".filter").forEach(x=>x.classList.remove("active"));b.classList.add("active");currentFilter=b.dataset.filter;render()}));
$$(".dot").forEach(b=>b.addEventListener("click",()=>showSlide(Number(b.dataset.i))));
let slide=0;
function showSlide(i){slide=i;$$(".slide").forEach((x,n)=>x.classList.toggle("active",n===i));$$(".dot").forEach((x,n)=>x.classList.toggle("active",n===i))}
setInterval(()=>showSlide((slide+1)%3),5000);
loadHotels();
