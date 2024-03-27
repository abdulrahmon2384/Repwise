let requirements = [];
let checkedValues = [];

function checkCheckbox(checkboxId) {
	var checkbox = document.getElementById(checkboxId);
	checkbox.checked = !checkbox.checked; // Toggle checkbox state
}



function fetchDataAndPopulate() {
	fetch("/api/user-info")
		.then((response) => response.json())
		.then((data) => {
			document.getElementById("username").textContent = data.name;
			document.getElementById("userid").textContent = data.id;
			document.getElementById("userole").textContent = data.roles;
		})
		.catch((error) => {
			console.error("Error fetching data:", error);
		});
}





function populateCategories(data) {
	var categories = document.getElementById("categories-list");
	categories.classList.add("categories-list");

	for (var category in data) {
		if (data.hasOwnProperty(category)) {
			var categoryItem = document.createElement("li");
			categoryItem.textContent = category;

			categoryItem.addEventListener("click", function () {
				var sublist = this.querySelector("ul");
				sublist.classList.toggle("sublist-active");
			});

			categories.appendChild(categoryItem);
			var descriptionsList = document.createElement("ul");

			data[category].forEach(function (item) {
				var descriptionItem = document.createElement("li");
				descriptionItem.textContent = item.description;
				descriptionsList.appendChild(descriptionItem);
			});

			categoryItem.appendChild(descriptionsList);
		}
	}
}




async function fetchDataAndPopulateCategories(apiUrl) {
	try {
		const response = await fetch(apiUrl);
		if (!response.ok) {
			throw new Error("Network response was not ok");
		}
		const data = await response.json();

		for (const category in data.categories) {
			for (const requirement in data.categories[category]) {
				requirements.push(data.categories[category][requirement]);
			}
		}

		if (requirements.length > 0) {
			requirements.sort((a, b) => a.timestamp - b.timestamp);
		}

		populateCategories(data.categories);
		fetchUserFeeds(requirements);
	} catch (error) {
		console.error("There was a problem with the fetch operation:", error);
	}
}

function fetchUserFeeds(requirements) {
	fetch("/api/userAgreementId")
		.then((response) => {
			if (!response.ok) {
				throw new Error("Network response was not ok");
			}
			return response.json();
		})
		.then((data) => {
			var userIds = [];

			for (let id in data.agreementid) {
				userIds.push(data.agreementid[id]);
			}
			console.log(userIds)
			console.log(requirements)
			populateUserFeeds(userIds, requirements);
		})
		.catch((error) => {
			console.error(
				"There was a problem with the fetch operation:",
				error,
			);
		});
}

function populateUserFeeds(userids, requirements) {
	//console.log(requirements.length)
	if (requirements.length == 0) {
		emptyDbOrUserAgreed("eMPTy", "userfeeds");
	} else if (userids.length == requirements.length) {
		//console.log("All requirements have been fetched");
		emptyDbOrUserAgreed("", "userfeeds");
	} else {
		var userFeeds = document.getElementById("userfeeds");
		userFeeds.innerHTML = "";

		for (let index in requirements) {
			//console.log(requirements[index])
			req = requirements[index];

			if (!userids.includes(req.id)) {
				var requirementItem = document.createElement("div");
				requirementItem.classList.add("requirement-item");
				requirementItem.innerHTML = `
						<div class="requirement-item">
							<div class="checkbox-heading">
								<label for="req1">${req.category}</label>
							</div>
							<div class="requirement-description"> <span >${req.description}</span></div>
							<div class="checkbox-container" onclick=handleCheckboxClick('${req.id}')>
								<div class="checkbox-inner-container" onclick="checkCheckbox('${req.id}')">
									<span >ok
										<input type="checkbox" id="${req.id}" value="${req.id}" class="custom-checkbox" onclick="handleCheckboxClick(this)"/>
									</span>
								</div>
							</div>
						</div>
				`;
				userFeeds.appendChild(requirementItem);
			}
		}
		var agreebuttonDiv = document.createElement("div");
		agreebuttonDiv.classList.add("agreement-section");
		agreebuttonDiv.innerHTML = `
					   <div class="subheading"><label>Agreement</label></div>
					   <div class="agreement-info">
						   By checking the boxes above, I agree to comply with the
						   stated requirements.
					   </div>
					   <button class="button" onclick="pushCheckedValues()" >
						   Agree
					   </button>
			`;
		userFeeds.appendChild(agreebuttonDiv);
	}
}



function emptyDbOrUserAgreed(message, DivId) {
	var parentDiv = document.getElementById(DivId);
	var innerDiv = document.createElement("div");

	parentDiv.innerHTML = "";
	parentDiv.classList.add("empty-div");
	innerDiv.classList.add("requirement-item");

	if (message == "eMPTy") {
		innerDiv.innerHTML = `
				<div class="empty-database">
					<div class="empty-database-content">
						<div class="empty-database-header">Requirements Not Available</div>
						<div class="empty-database-message">The database is empty</div>
					</div>
				</div>
		`;
	} else {
		innerDiv.innerHTML = `
				<div class="agreement-success">
					<div class="agreement-success-content">
						<i class="fas fa-check-circle"></i>
						<span>Requirement Agreed</span>
					</div>
				</div>
		`;
	}
	parentDiv.appendChild(innerDiv);
}

// Function to handle checkbox click
function handleCheckboxClick(checkbox) {
	if (checkbox) {
		if (!checkedValues.includes(checkbox)) {
			checkedValues.push(checkbox);
		} else {
			index = checkedValues.indexOf(checkbox);
			checkedValues.splice(index, 1);
		}
	}//console.log(checkedValues)
}

// Function to push checked values to Flask API
function pushCheckedValues() {
	//console.log(checkedValues)
	fetch("/api/checkbox-values", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ values: checkedValues }),
	})
		.then((response) => {
			if (response.ok) {
				checkedValues = [];
				fetchUserFeeds(requirements);
			} else {
				console.error("Failed to send checked values.");
			}
		})
		.catch((error) => {
			console.error("Error:", error);
		});
}



window.onload = function () {
	fetchDataAndPopulateCategories("/api/all-feeds");
	fetchDataAndPopulate();
};
