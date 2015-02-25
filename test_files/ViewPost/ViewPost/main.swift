import Foundation

//create a mutable request with api view path /viewpost, set method to POST
//kyle
//var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.121:8000/viewpost")!)
//trenton
var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.3:8000/viewpost/")!)
request.HTTPMethod = "POST"

//open NSURLSession
var session = NSURLSession.sharedSession()

//parameter values
//common post information
var postid = "178"
var category = "Household"


//this is the parameters array that will be formulated as JSON.
// We need both postid and category
var params = ["post_id":postid,          //post id so we find the post
    "category":category]                 //category so we know what table to search
    as Dictionary<String,AnyObject>


//Load body with JSON serialized parameters, set headers for JSON! (Star trek?)
var err: NSError?
request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: &err)
request.addValue("application/json", forHTTPHeaderField: "Content-Type")
request.addValue("application/json", forHTTPHeaderField: "Accept")


//define NSURLSession data task with completionHandler call back function
var task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
    
    //read the message from the response
    var title = ""
    var description = ""
    var price = ""
    var departure_date_time = ""
    var return_date_time = ""
    var round_trip = false
    var trip = ""
    var gonzaga_email = ""
    var pref_email = ""
    var call = ""
    var text = ""
    var isbn = ""
    var location = ""
    var date_time = ""
    var imageString: [String] = ["","",""]
    var json = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? NSDictionary
    if(err != nil) {
        println(err!.localizedDescription)
        let jsonStr = NSString(data: data, encoding: NSUTF8StringEncoding)
        println("Error could not parse JSON: '\(jsonStr)'")
    }
    else{
        if let parseJSON = json as? Dictionary<String,AnyObject>{
            title = parseJSON["title"] as String
            description = parseJSON["description"] as String
            price = parseJSON["price"] as String
            gonzaga_email = parseJSON["gonzaga_email"] as String
            pref_email = parseJSON["pref_email"] as String
            call = parseJSON["call"] as String
            text = parseJSON["text"] as String
            
            println(price)

            if category == "Books"{
                isbn = parseJSON["isbn"] as String
            }
          
            if category == "Events" || category == "Services"{
                location = parseJSON["location"] as String
                date_time = parseJSON["date_time"] as String
            }

            if category == "Ride Shares"{
                departure_date_time = parseJSON["departure_date_time"] as String
                round_trip = parseJSON["round_trip"] as Bool
                trip = parseJSON["trip"] as String
                if round_trip{
                    return_date_time = parseJSON["return_date_time"] as String
                }
            }
            //The Three images are processed here
            imageString[0] = parseJSON["image1"]! as String
            imageString[1] = parseJSON["image2"]! as String
            imageString[2] = parseJSON["image3"]! as String
            if !imageString[0].isEmpty {
                let imageData1 = NSData(base64EncodedString: imageString[0], options: NSDataBase64DecodingOptions.IgnoreUnknownCharacters)!
                    
                //do stuff with the image here
            }
            else{
                //CASE IN WHICH THE POST HAD NO IMAGE 1
            }
            if !imageString[1].isEmpty {
                let imageData2 = NSData(base64EncodedString: imageString[1], options: NSDataBase64DecodingOptions.IgnoreUnknownCharacters)!
                
                //do stuff with the image here
            }
            else{
                //CASE IN WHICH THE POST HAD NO IMAGE 2
            }
            if !imageString[2].isEmpty {
                let imageData3 = NSData(base64EncodedString: imageString[2], options: NSDataBase64DecodingOptions.IgnoreUnknownCharacters)!
                
                //do stuff with the image here
            }
            else{
                //CASE IN WHICH THE POST HAD NO IMAGE 3
            }

        }
    }
    
    //downcast NSURLResponse object to NSHTTPURLResponse
    if let httpResponse = response as? NSHTTPURLResponse {
        
        //get the status code
        var status_code = httpResponse.statusCode
        
        //200 = OK: user created, carry on!
        if(status_code == 200){
            
            print("Title = ")
            println(title)
            print("Description = ")
            println(description)
            print("Category = ")
            println(category)
            print("Price = ")
            println(price)
            print("Gonzaga email = ")
            println(gonzaga_email)
            print("Pref email = ")
            println(pref_email)
            print("Call = ")
            println(call)
            print("Text = ")
            println(text)
            if category == "Ride Shares"{
                print("Departure Date Time = ")
                println(departure_date_time)
                print("Round Trip = ")
                println(round_trip)
                print("Trip = ")
                println(trip)
                if round_trip{
                    print("Return Date Time = ")
                    println(return_date_time)
                }
            }
            if category == "Events" || category == "Services"{
                print("Date Time = ")
                println(date_time)
                print("Location = ")
                println(location)
            }
            if category == "Books"{
                print("ISBN = ")
                println(isbn)
            }

        }
            
            //400 = BAD_REQUEST: error in creating user, display error!
        else if(status_code == 400){
            println(title)
        }
            
            //500 = INTERNAL_SERVER_ERROR. Oh snap *_*
        else if(status_code == 500){
            println("The server is down! Call the fire department!")
        }
        
        
    } else {
        println("Error in casting response, data incomplete")
    }
    
    
    
})
task.resume()


sleep(5)

