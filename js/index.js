const DomElement = (selector) => {
	try {
		if (document.querySelector(selector))
			return document.querySelector(selector);
		throw new Error(`${selector} does'nt exist or it's not a valid selector`);
	} catch (err) {
		console.log(err);
	}
};

const openBtn = DomElement("#open-btn");
const navbar = DomElement("#navbar");
const display = DomElement(".display");
const onLightBtn = DomElement(".light-btn-on");
const offLightBtn = DomElement(".light-btn-off");
const linkItems = document.querySelectorAll(".link-item");
const header = DomElement(".header");

//navbar behavior
document.body.addEventListener("click", function (event) {
	const id = event.target.id;
	console.log(id);
	if (id == "bar-open") {
		navbar.classList.toggle("hide-navbar");
	} else {
		navbar.classList.add("hide-navbar");
	}
});

navbar.addEventListener("click", (event) => {
	const classList = event.target.classList;
	if (classList.contains("nav-link")) {
		linkItems.forEach((item) => {
			item.classList.remove("active");
		});
		event.target.parentNode.classList.add("active");
	}
});

navbar.style.top = `${header.getBoundingClientRect().height}px`;

//switch between light and dark mode

onLightBtn.addEventListener("click", () => {
	document.body.classList.add("dark-mode");
	offLightBtn.classList.remove("hide-btnLightDarkMode");
	onLightBtn.classList.add("hide-btnLightDarkMode");
});

offLightBtn.addEventListener("click", () => {
	document.body.classList.remove("dark-mode");
	offLightBtn.classList.add("hide-btnLightDarkMode");
	onLightBtn.classList.remove("hide-btnLightDarkMode");
});

/* smooth scroll behavior*/
const scrollLinks = document.querySelectorAll(".scroll-link");
scrollLinks.forEach((link) => {
	link.addEventListener("click", (e) => {
		// prevent default
		e.preventDefault();
		// navigate to specific spot
		const id = e.currentTarget.getAttribute("href").slice(1);
		const element = document.getElementById(id);
		const headerHeight = header.getBoundingClientRect().height;
		let position = element.offsetTop - headerHeight;

		window.scrollTo({
			top: position,
		});
		// close nav
		navbar.classList.remove("hide-navbar");
	});
});
