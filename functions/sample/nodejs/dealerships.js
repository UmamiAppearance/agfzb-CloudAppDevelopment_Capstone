const Cloudant = require('@cloudant/cloudant');

function compileResponse(msg, statusCode=200) {
    const response = {
        headers: { 
            "Content-Type": "application/json"  
        }, 
        statusCode: String(statusCode)
    }

    if (statusCode !== 200) {
        response.body = { error: msg };
    } else {
        response.body = { data: msg };
    }

    return response;
}

async function main(params) {
    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: {
            iamauth: {
                iamApiKey: params.IAM_API_KEY
            }
        }
    });

    const dealerships_db = cloudant.db.use("dealerships")
    
    let query;
    const fields = ["id", "city", "state", "st", "address", "zip", "lat", "long", "short_name", "full_name"];
    const stateFilter = params.hasOwnProperty("state");
    const getID = params.hasOwnProperty("dealerId");
    
    if (stateFilter) {
        query = {
            selector: {
                st: {"$eq": params.state },
            },
            fields: fields
        };
    } else if (getID) {
        query = {
            selector: {
                id: {"$eq": parseInt(params.dealerId, 10) },
            },
            fields: fields
        };
    } else {
        query = {
            selector: {},
            fields: fields
        };
    }
    
    let dealershipsList;
    if ((stateFilter && !params.state) || (getID && !params.dealerId)) {
        dealershipsList = { bookmark: "nil" };
    } else {
        try {
            dealershipsList = await dealerships_db.find(query);
        } catch (error) {
            return compileResponse(error.description, 500);
        }
    }
    
    let response;
    if (dealershipsList.bookmark !== "nil") {
        response = compileResponse(dealershipsList);
    } else {
        let message;
        if (stateFilter) {
            message ="The state does not exist";
        } else if (getID) {
            message ="No match found for the given id";
        } else {
            message = "The database is empty";
        }
        response = compileResponse(message, 404);
    }
    
    return response;
}
