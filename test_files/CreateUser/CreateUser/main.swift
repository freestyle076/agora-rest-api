//
//  main.swift
//  LdapAuth
//
//  Created by Kyle Handy on 10/31/14.
//  Copyright (c) 2014 Kyle Handy. All rights reserved.
//

import Foundation



//var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.121:8000/ldapauth/")!)
var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.133:8000/ldapauth/")!)
var session = NSURLSession.sharedSession()
request.HTTPMethod = "POST"

var username = "khandy" //set username value here
var password =  "Rusty3220" //set password value here

var params = ["username":username, "password":password] as Dictionary<String, String>

var err: NSError?
request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: &err)
request.addValue("application/json", forHTTPHeaderField: "Content-Type")
request.addValue("application/json", forHTTPHeaderField: "Accept")


var task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
    
    var jsonStr = NSString(data: data, encoding: NSUTF8StringEncoding)
    var err: NSError?
    var json = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? NSDictionary
    
    if(err != nil) {
        println(err!.localizedDescription)
        let jsonStr = NSString(data: data, encoding: NSUTF8StringEncoding)
        println("Error could not parse JSON: '\(jsonStr)'")
    }
        
    else {
        // The JSONObjectWithData constructor didn't return an error. But, we should still
        // check and make sure that json has a value using optional binding.
        if let parseJSON = json as? Dictionary<String,AnyObject>{
            // Okay, the parsedJSON is here, let's get the value for 'success' out of it
            if let message = parseJSON["Message"] as? String{
                println("Message: \(message)")
            }
            if let email = parseJSON["email"] as? String{
                println("email: \(email)")
            }
            if let username = parseJSON["username"] as? String{
                println("username: \(username)")
            }
            
        }
        else {
            // Woa, okay the json object was nil, something went worng. Maybe the server isn't running?
            let jsonStr = NSString(data: data, encoding: NSUTF8StringEncoding)
            println("Error could not parse JSON: \(jsonStr)")
        }
    }
    
    /*
    if let httpResponse = response as? NSHTTPURLResponse {
    var status_code = httpResponse.statusCode
    println("response \(httpResponse)")
    
    //200 = OK, valid credentials
    if(status_code == 200){
    println("Valid credentials! Carry on to main page...")
    }
    
    //400 = BAD_REQUEST, invalid crentials
    else if(status_code == 400){
    println("Invalid credentials, you are not allowed in!")
    }
    
    //500 = INTERNAL_SERVER_ERROR. Oh snap *_*
    else if(status_code == 500){
    println("The server is down! Call the fire!")
    }
    
    
    } else {
    println("Error in casting response, data incomplete")
    }*/
    
})

task.resume()



sleep(15)
