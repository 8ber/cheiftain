function setTable(tdName1, tdName2, tdName3, tdName4="", tdName5="")
{
	let table = document.getElementById("mainTable")
    let tr = document.createElement("tr")
    table.appendChild(tr)
    let tdName = document.createElement("td")
    tdName.innerText = tdName1
    tr.appendChild(tdName)
    let tdProducts = document.createElement("td")
    tdProducts.innerText = tdName2
    tr.appendChild(tdProducts)
    let tdDates = document.createElement("td")
    tdDates.innerText = tdName3
    tr.appendChild(tdDates)
    if (tdName4 && tdName5)
    {
        let tdDates1 = document.createElement("td")
        tdDates1.innerText = tdName4
        tr.appendChild(tdDates1)
        let tdDates2 = document.createElement("td")
        tdDates2.innerText = tdName5
        tr.appendChild(tdDates2)
    }
}

var isVisible = false
function showHide() 
{
	let form = document.getElementsByClassName("formToHide")
    isVisible = !isVisible
    if (isVisible) {
    	for (let e of form)
    		{ e.style.display = "none" } }
     else {
    	for (let e of form)
    		{ e.style.display = "inline" } }
}

function becomeAghost()
{
    localStorage.removeItem("token");
    sessionStorage.clear();
}

async function customersPageGenerate() 
{    
    let token = localStorage.getItem("token");
    let fetchParams = {  
        method : "GET",
        headers : {"Content-type"  :"application/json",
       "x-access-token" : token}
       }
    let resp = await fetch("http://127.0.0.1:5000/customers", fetchParams);
    let customersData = await resp.json();
    let table = document.getElementById("mainTable")

    customersData.forEach(customer => {

    let tr = document.createElement("tr")
    table.appendChild(tr)
   
    let tdName = document.createElement("td")
    tr.appendChild(tdName)

    let radio = document.createElement("input")
    radio.type = "radio"
    radio.style.display = "none"
    radio.name = "customers names"
    radio.value = `${customer.customerID}`
    radio.className = `formToHide`
    tdName.appendChild(radio)

    let name = document.createTextNode(`${customer.firstname} ${customer.lastname}`)
    tdName.appendChild(name)

    let tdProducts = document.createElement("td")
    tr.appendChild(tdProducts)
    let tdDates = document.createElement("td")
    tr.appendChild(tdDates) 

    search({customerID : `${customer.customerID}`}).then((data)=>
    {
        data.forEach(prod=> { 
        let productName = document.createElement("a")
        productName.innerText = `${prod.name}`
        productName.href = "editProduct.html"
        productName.onclick = () => { sessionStorage.setItem("productID", `${prod.productID}`);
    }
        let brake = document.createElement("br")
        tdProducts.appendChild(productName)
        productName.appendChild(brake) 
        let dat = document.createTextNode(`${prod.date}`)
        let brake1 = document.createElement("br")
        tdDates.appendChild(dat)
        tdDates.appendChild(brake1)
        })

     })  //END OF THEN
    }) //CUSTOMERS FOREACH

    let mainDiv = document.getElementById("contentBox")
    let newDeal = document.createElement("span")
    mainDiv.appendChild(newDeal)
    newDeal.innerText = "➤Want to buy more? click here"
    newDeal.id = "BuyBtn"
    newDeal.onclick = () => showHide() 

    let brake = document.createElement("br")
    mainDiv.appendChild(brake)

    products().then(allProducts =>{
    	let selectProduct = document.createElement("select");
    	selectProduct.id = "selectProduct"
    	selectProduct.style.display = "none"
    	selectProduct.className = "formToHide"
    	mainDiv.appendChild(selectProduct)

    	allProducts.forEach(prod => {
    		let option = document.createElement("option");
			option.text = `${prod.name}`
			option.value = `${prod.productID}`
			selectProduct.add(option);
    	})

    	buyButton = document.createElement("input")
    	mainDiv.appendChild(buyButton)
    	buyButton.style.display = "none"
    	buyButton.className = "formToHide"
    	buyButton.type = "button"
    	buyButton.value = "Buy"
    	response = document.createElement("span")
    	response.id = "status"
    	
    	buyButton.onclick = () => { 
    		let prodID = document.getElementById("selectProduct")
    		prodIDvalue = prodID.options[prodID.selectedIndex].value;
    		radioButtons = document.getElementsByName("customers names")
    		for (let button of radioButtons) {
    			if (button.checked)
    			{
    				custID = button.value
    			}
    		}
    		let dealDetails = { "productID" : `${prodIDvalue}`,
    							"customerID" : `${custID}` }

    		newPurchase(dealDetails).then(resp => resp.json()).then(data=>{
                response.innerText = ` - ${data}`
            })
    			
    	}
    	mainDiv.appendChild(response)
    })
} 

async function newPurchase(purchaseDataObj) 
{    
    let token = localStorage.getItem("token");
    // let purchaseDataObj = {customerID : id}
    let fetchParams = 
    {  
    method : "POST",
    body : JSON.stringify(purchaseDataObj),
    headers : {"Content-type"  :"application/json",
    "x-access-token" : token}}
    let response = await fetch("http://127.0.0.1:5000/new_purchase", fetchParams)
    return response
}


async function search(obj) 
{
    let token = localStorage.getItem("token");
    let fetchParams = 
    {  
    method : "POST",
    body : JSON.stringify(obj),
    headers : {"Content-type"  :"application/json",
    "x-access-token" : token}    }
    let response = await fetch("http://127.0.0.1:5000/search", fetchParams)
    let Data = await response.json();
    return Data
}


async function products() 
{    
    let token = localStorage.getItem("token");
    //get Ajax request to server:
    let fetchParams = {  
                        method : "GET",
                        headers : {"Content-type"  :"application/json",
                       "x-access-token" : token}
                       }
   let resp = await fetch("http://127.0.0.1:5000/products", fetchParams);
   let productsData = await resp.json();
   return productsData
 }


async function editProduct()
{
    let prodID = sessionStorage.getItem("productID");
    let allProducts = await products()
    let productDetails = allProducts.filter(product => product.productID == prodID)
    return productDetails[0]

}

async function customers() 
{    
    let token = localStorage.getItem("token");
    //get Ajax request to server:
    let fetchParams = {  
                        method : "GET",
                        headers : {"Content-type"  :"application/json",
                       "x-access-token" : token}
                       }
   let resp = await fetch("http://127.0.0.1:5000/customers", fetchParams);
   let customersData = await resp.json();
   return customersData
 }

 async function purchases() 
 {
    let token = localStorage.getItem("token");
    //get Ajax request to server:
    let fetchParams = {  
                        method : "GET",
                        headers : {"Content-type"  :"application/json",
                       "x-access-token" : token}
                       }
   let resp = await fetch("http://127.0.0.1:5000/purchases", fetchParams);
   let purchasesData = await resp.json();
   return purchasesData
 }

async function editCustomer()
{
    let custID = sessionStorage.getItem("customerID");
    let allCustomers = await customers()
    let customerDetails = allCustomers.filter(customer => customer.customerID == custID)
    return customerDetails[0]

}

async function productsPageGenerate() 
{    
    let token = localStorage.getItem("token");
     //post Ajax request to server:
     let fetchParams = {  
                         method : "GET",
                         headers : {"Content-type"  :"application/json",
                        "x-access-token" : token}
                        }
    let resp = await fetch("http://127.0.0.1:5000/products", fetchParams);
    let productsData = await resp.json();
    let table = document.getElementById("mainTable")

    productsData.forEach(product => {

    let tr = document.createElement("tr")
    table.appendChild(tr)
   
    let tdName = document.createElement("td")
    tr.appendChild(tdName)

    let radio = document.createElement("input")
    radio.type = "radio"
    radio.style.display = "none"
    radio.name = "products names"
    radio.value = `${product.productID}`
    radio.className = `formToHide`
    tdName.appendChild(radio)

    let name = document.createTextNode(`${product.name}`)
    tdName.appendChild(name)

    let tdPrice = document.createElement("td")
    tdPrice.innerText = `${product.price}`
    tr.appendChild(tdPrice)

    let tdQuantity = document.createElement("td")
    tdQuantity.innerText = `${product.quantity}`
    tr.appendChild(tdQuantity)

    let tdCustomers = document.createElement("td")
    tr.appendChild(tdCustomers)
    let tdDates = document.createElement("td")
    tr.appendChild(tdDates) 

    search({productID:`${product.productID}`}).then((data)=>
    {
        data.forEach(customer=> { 
        let customerName = document.createElement("a")
        customerName.innerText = `${customer.firstname} ${customer.lastname}`
        customerName.href = "editCustomer.html"
        customerName.onclick = () => { sessionStorage.setItem("customerID", `${customer.customerID}`);
    }
        let brake = document.createElement("br")
        tdCustomers.appendChild(customerName)
        customerName.appendChild(brake) 
        let dat = document.createTextNode(`${customer.date}`)
        let brake1 = document.createElement("br")
        tdDates.appendChild(dat)
        tdDates.appendChild(brake1)
        })

     })  //END OF THEN
    }) //PRODUCTS FOREACH


    let mainDiv = document.getElementById("contentBox")
    let numOfpurchases = document.createElement("span")
    mainDiv.appendChild(numOfpurchases)
    mainDiv.appendChild(document.createElement("br")) 


    purchases().then(data=>{
        numOfpurchases.innerText = `Current Number of transactions: ${data.length}`
    })


    let newDeal = document.createElement("span")
    mainDiv.appendChild(newDeal)
    newDeal.innerText = "➤Want to buy more? click here"
    newDeal.id = "BuyBtn"
    newDeal.onclick = () => showHide() 

    let brake = document.createElement("br")
    mainDiv.appendChild(brake)

    customers().then(allCustomers =>{
    	let selectCustomer = document.createElement("select");
    	selectCustomer.id = "selectCustomer"
    	selectCustomer.style.display = "none"
    	selectCustomer.className = "formToHide"
    	mainDiv.appendChild(selectCustomer)

    	allCustomers.forEach(customer => {
    		let option = document.createElement("option");
			option.text = `${customer.firstname} ${customer.lastname}`
			option.value = `${customer.customerID}`
			selectCustomer.add(option);
    	})

    	buyButton = document.createElement("input")
    	mainDiv.appendChild(buyButton)
    	buyButton.style.display = "none"
    	buyButton.className = "formToHide"
    	buyButton.type = "button"
    	buyButton.value = "Buy"
    	response = document.createElement("span")
    	response.id = "status"
    	
    	buyButton.onclick = () => { 
    		let custID = document.getElementById("selectCustomer")
    		custIDvalue = custID.options[custID.selectedIndex].value;
    		radioButtons = document.getElementsByName("products names")
    		for (let button of radioButtons) {
    			if (button.checked)
    			{
    				prodID = button.value
    			}
    		}
    		let dealDetails = { "customerID" : `${custIDvalue}`,
    							"productID" : `${prodID}` }

    		newPurchase(dealDetails).then(resp => resp.json()).then(data=>{
                response.innerText = ` - ${data}`
    		})
    	}
    	mainDiv.appendChild(response)
    })
} 