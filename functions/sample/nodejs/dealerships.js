const Cloudant = require('@cloudant/cloudant');

function compileResponse(msg, statusCode=400) {
    const response = {
        headers: { 
            "Content-Type": "application/json"  
        }, 
        statusCode: String(statusCode)
    }
    if (statusCode !== 400) {
        response.body = { error: msg };
    } else {
        response.body = msg;
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
    const fields = ["id", "city", "state", "st", "address", "zip", "lat", "long"];
    const stateFilter = params.hasOwnProperty("state");
    if (stateFilter) {
        query = {
            selector: {
                st: {"$eq": params.state },
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
    if (stateFilter && !params.state) {
        dealershipsList = { docs: [] };
    } else {
        try {
            dealershipsList = await dealerships_db.find(query);
        } catch (error) {
            return compileResponse(error.description, 500);
        }
    }
    let response;
    if (dealershipsList.docs.length) {
        response = compileResponse(dealershipsList.docs);
    } else {
        const message = (stateFilter) ? "The state does not exist" :  "The database is empty";
        response = compileResponse(message, 404);
    }
    return response;
}