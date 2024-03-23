// validate user
async function validateUser() {
	try {
		const response = await fetch("/api/validate");
		const isValidUser = await response.json();
		return isValidUser;
	} catch (error) {
		console.error("Error validating user:", error);
		return false;
	}
}

// get checked checkbox values and username
function getCheckedValues() {
	const username = document
		.getElementById("user-info")
		.getAttribute("user-name");
	const checkboxes = document.querySelectorAll(
		'#requirementsContainer input[type="checkbox"]',
	);
	const checkedValues = [];
	let countValues = 0;

	checkboxes.forEach(function (checkbox) {
		if (checkbox.checked) {
			const value = checkbox.value;
			checkedValues.push(value);
			countValues++;
		}
	});

	let numOfCheckboxes = checkboxes.length;

	if (countValues !== numOfCheckboxes) {
		alert("All checkboxes must be checked");
	} else {
		//console.log(checkedValues, username)
		return [checkedValues, username];
	}
}

// send data to Flask API
async function sendDataToAPI(values) {
	try {
		const response = await fetch("/api/store-values", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ values }),
		});

		if (!response.ok) {
			throw new Error("Failed to store values");
		}

		const data = await response.json();
		console.log("Response from Flask API:", data);
	} catch (error) {
		console.error("Error sending data to Flask API:", error);
	}
}

function clearAndAppendHTMLToDiv() {
	var divElement = document.getElementById("colapsable-div");
	divElement.innerHTML = "";

	var row = `
		<div class="agreement-success">
            <div class="agreement-success-content">
                <i class="fas fa-check-circle"></i>
                <span>Requirement Agreed</span>
            </div>
       </div>
	`;

	divElement.innerHTML += row;
}

// main function
async function processCheckboxValues() {
	const [checkedValues, username] = getCheckedValues();
	if (checkedValues.length > 0) {
		const isValidUser = await validateUser();
		if (isValidUser) {
			console.log(checkedValues, username)
			await sendDataToAPI([checkedValues, username]);
		} else {
			alert("Invalid user. Please log in again.");
		}
	}
}


//onlcick event function
async function processCheckboxBeforClear() {
	await processCheckboxValues(); 
	clearAndAppendHTMLToDiv(); 
}


async function fetchCategoriesAndPopulateList(divId) {
	try {
		const response = await fetch("/api/categories");
		const data = await response.json();
		populateCategoriesInDiv(data.categories, divId);
	} catch (error) {
		console.error("Error fetching categories:", error);
	}
}

function populateCategoriesInDiv(categories, divId) {
	const div = document.getElementById(divId);
	if (!div) {
		console.error("Div with specified ID not found.");
		return;
	}

	const list = document.createElement("ul");
	list.classList.add("category-list"); 

	for (const category in categories) {
		const categoryItem = document.createElement("li");
		categoryItem.textContent = category;
		categoryItem.classList.add("category-item"); 

		const descriptionList = document.createElement("ul");
		descriptionList.classList.add("description-list");

		for (const item of categories[category]) {
			const descriptionItem = document.createElement("li");
			descriptionItem.textContent = item.description;
			descriptionItem.classList.add("description-item"); 
			descriptionList.appendChild(descriptionItem);
		}

		categoryItem.appendChild(descriptionList);
		list.appendChild(categoryItem);

		categoryItem.addEventListener("click", () => {
			descriptionList.classList.toggle("expanded");
		});
	}

	div.appendChild(list);
}

// Call the function to fetch and populate categories inside the specified div
fetchCategoriesAndPopulateList("categories-list");






function fetchUserInfo() {
	fetch('/api/user-info')
	.then(response => response.json())
	.then(data => {
		// Populate the HTML elements with the fetched data
		document.getElementById('username').textContent = data.name;
		document.getElementById('userid').textContent = data.id;
		document.getElementById('userole').textContent = data.roles;
	})
	.catch(error => console.error('Error fetching user info:', error));
}

// Call the fetchUserInfo function when the page loads
window.onload = fetchUserInfo;


