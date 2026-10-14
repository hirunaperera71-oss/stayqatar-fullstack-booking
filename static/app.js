let stays=[], experiences=[], currentFilter="all", expFilter="all";
let favorites=JSON.parse(localStorage.getItem("stayqatar-favorites")||"[]");
const $=s=>document.querySelector(s), $$=s=>document.querySelectorAll(s);
function toast(msg){const t=$("#toast");t.textContent=msg;t.classList.add("show");setTimeout(()=>t.classList.remove("show"),3200)}
async function loadStays(){
 const p=new URLSearchParams(),q=$("#where").value.trim();
 if(q)p.set("q",q);if(currentFilter!=="all")p.set("category",currentFilter);
 if($("#guests").value)p.set("guests",$("#guests").value);
 if($("#maxPrice").value)p.set("max_price",$("#maxPrice").value);
 p.set("sort",$("#sort").value);
 const r=await fetch("/api/stays?"+p.toString());stays=await r.json();renderStays();
}
async function loadExperiences(){
 const p=new URLSearchParams();if(expFilter!=="all")p.set("category",expFilter);
 experiences=await(await fetch("/api/experiences?"+p.toString())).json();renderExperiences();
}
function renderStays(){
 $("#results").innerHTML=stays.length?stays.map(h=>`<article class="card" onclick="openItem('stay',${h.id})"><div class="card-img" style="background-image:url('${h.image}')"><span class="card-badge">${h.tag}</span><button class="heart ${favorites.includes('s'+h.id)?'saved':''}" aria-label="Save favourite" onclick="event.stopPropagation();toggleFav(${h.id})">${favorites.includes('s'+h.id)?'♥':'♡'}</button></div><div class="card-body"><div class="card-top"><div><h3>${h.name}</h3><div class="location">${h.location}</div></div><div class="rating">★ ${h.rating}</div></div><div class="price"><strong>QAR ${h.price.toLocaleString()}</strong> / night <span class="type">${h.type}</span></div><div class="card-extra">${h.guests} guests · ${h.bedrooms} bedroom${h.bedrooms>1?'s':''}</div></div></article>`).join(""):'<div class="empty">No stays match your search. Try changing the filters.</div>';
 $("#favCount").textContent=favorites.length;
}
function renderExperiences(){
 $("#experienceResults").innerHTML=experiences.length?experiences.map(x=>`<article class="experience-card" onclick="openItem('experience',${x.id})"><div class="exp-image" style="background-image:url('${x.image}')"><span class="card-badge">${x.category}</span></div><div class="exp-body"><h3>${x.name}</h3><p>⌖ ${x.location} · ${x.duration} · ★ ${x.rating}</p><div class="exp-price"><span>Local-led experience</span><strong>QAR ${x.price} / person</strong></div></div></article>`).join(""):'<div class="empty">No experiences in this category.</div>';
}
function toggleFav(id){
 const key='s'+id;favorites=favorites.includes(key)?favorites.filter(x=>x!==key):[...favorites,key];
 localStorage.setItem("stayqatar-favorites",JSON.stringify(favorites));renderStays();toast(favorites.includes(key)?"Added to favourites":"Removed from favourites");
}
function showFavorites(){
 const ids=favorites.filter(x=>x.startsWith('s')).map(x=>Number(x.slice(1)));
 if(!ids.length){toast("Tap the heart on a stay to save a favourite.");return}
 $("#results").innerHTML=stays.filter(s=>ids.includes(s.id)).map(h=>`<article class="card" onclick="openItem('stay',${h.id})"><div class="card-img" style="background-image:url('${h.image}')"><span class="card-badge">Your favourite</span><button class="heart saved" onclick="event.stopPropagation();toggleFav(${h.id})">♥</button></div><div class="card-body"><h3>${h.name}</h3><div class="location">${h.location}</div><div class="price"><strong>QAR ${h.price}</strong> / night</div></div></article>`).join("")||'<div class="empty">Your favourites are not in the current search. Reset filters to view them.</div>';
 $("#stays").scrollIntoView({behavior:"smooth"});
}
function openItem(type,id){
 const list=type==="stay"?stays:experiences;const item=list.find(x=>x.id===id);if(!item)return;
 const isStay=type==="stay";
 $("#modalContent").innerHTML=`<img class="detail-img" src="${item.image}" alt="${item.name}"><div class="detail-body"><div class="type">${isStay?item.type:item.category} · ★ ${item.rating}</div><h2>${item.name}</h2><div class="location">⌖ ${isStay?item.location:item.location+(item.duration?' · '+item.duration:'')}</div><p>${item.desc}</p>${isStay?`<div class="amenities">${item.amenities.map(a=>`<span>${a}</span>`).join("")}</div>`:''}<div class="detail-grid"><div><b>QAR ${item.price.toLocaleString()}</b> ${isStay?'/ night':'/ person'}</div><div>${isStay?'Up to '+item.guests+' guests':item.duration}</div></div><h3>Request a booking</h3><form class="book-form" onsubmit="submitBooking(event,'${type}',${item.id})"><input name="name" placeholder="Full name" required><input name="email" type="email" placeholder="Email address" required><label class="form-label">${isStay?'Check-in date':'Experience date'}<input name="checkin" type="date" min="${new Date().toISOString().slice(0,10)}" required></label>${isStay?'<label class="form-label">Check-out date<input name="checkout" type="date" required></label>':''}<label class="form-label">Guests / people<input name="guests" type="number" min="1" max="${isStay?item.guests:20}" value="2" required></label><button>Send booking request →</button></form></div>`;
 $("#modal").classList.remove("hidden");
}
async function submitBooking(e,type,id){
 e.preventDefault();const d=Object.fromEntries(new FormData(e.target).entries());d.item_type=type;d.item_id=id;d.guests=Number(d.guests);
 if(type==="stay"&&d.checkout<=d.checkin){toast("Check-out must be after check-in.");return}
 const r=await fetch("/api/book",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(d)});const out=await r.json();
 if(out.ok){closeModal();toast(`Request saved · ${out.reference} · Total QAR ${out.total}`)}else toast(out.message||"Unable to save booking request.");
}
function closeModal(){$("#modal").classList.add("hidden")}
$("#closeModal").addEventListener("click",closeModal);$("#modal").addEventListener("click",e=>{if(e.target.id==="modal")closeModal()});
$("#searchForm").addEventListener("submit",async e=>{e.preventDefault();await loadStays();$("#stays").scrollIntoView({behavior:"smooth"})});
$("#stayFilters").addEventListener("click",e=>{const b=e.target.closest("[data-filter]");if(!b)return;currentFilter=b.dataset.filter;$$("[data-filter]").forEach(x=>x.classList.toggle("active",x===b));loadStays()});
$("#experienceFilters").addEventListener("click",e=>{const b=e.target.closest("[data-exp]");if(!b)return;expFilter=b.dataset.exp;$$("[data-exp]").forEach(x=>x.classList.toggle("active",x===b));loadExperiences()});
$("#sort").addEventListener("change",loadStays);$("#maxPrice").addEventListener("change",loadStays);
$("#resetFilters").addEventListener("click",()=>{$("#where").value="";$("#guests").value="";$("#maxPrice").value="";$("#sort").value="recommended";currentFilter="all";$$("[data-filter]").forEach(x=>x.classList.toggle("active",x.dataset.filter==="all"));loadStays();toast("Filters reset")});
$("#favoritesBtn").addEventListener("click",showFavorites);
$("#newsletterForm").addEventListener("submit",async e=>{e.preventDefault();const email=$("#newsletterEmail").value;const r=await fetch("/api/newsletter",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email})});const out=await r.json();toast(out.message);if(out.ok)$("#newsletterEmail").value=""});
$("#menuBtn").addEventListener("click",()=>$("#mainNav").classList.toggle("open"));$$('#mainNav a').forEach(a=>a.addEventListener("click",()=>$("#mainNav").classList.remove("open")));
$$(".dot").forEach(b=>b.addEventListener("click",()=>showSlide(Number(b.dataset.i))));let slide=0;
function showSlide(i){slide=i;$$(".slide").forEach((x,n)=>x.classList.toggle("active",n===i));$$(".dot").forEach((x,n)=>x.classList.toggle("active",n===i))}
setInterval(()=>showSlide((slide+1)%3),5500);
loadStays();loadExperiences();
