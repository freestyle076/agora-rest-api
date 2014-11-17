//
//  main.swift
//  LdapAuth
//
//  Created by Kyle Handy on 10/31/14.
//  Copyright (c) 2014 Kyle Handy. All rights reserved.
//

import Foundation



var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.121:8000/ldapauth/")!)
//var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.133:8000/ldapauth/")!)
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
    
    //variables to store incoming data
    var username = ""
    var first_name = ""
    var last_name = ""
    var g_email = ""
    var p_email = ""
    var phone = ""
    
    
    var status_code = (response as NSHTTPURLResponse).statusCode
    
    var jsonStr = NSString(data: data, encoding: NSUTF8StringEncoding)
    var err: NSError?
    var json = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? NSDictionary

    //check for error in deserialization
    if(err != nil) {
        println(err!.localizedDescription)
        let jsonStr = NSString(data: data, encoding: NSUTF8StringEncoding)
        println("Error could not parse JSON: '\(jsonStr)'")
    }
    //else parse JSON and receive user data values
    else {
        //parse JSON for data values
        if let parseJSON = json as? Dictionary<String,AnyObject>{
            if let _username = parseJSON["username"] as? String{
                username = _username
            }
            if let first = parseJSON["first_name"] as? String{
                first_name = first
            }
            if let last = parseJSON["last_name"] as? String{
                last_name = last
            }
            if let _g_email = parseJSON["g_email"] as? String{
                g_email = _g_email
            }
            if let _p_email = parseJSON["p_email"] as? String{
                p_email = _p_email
            }
            if let _phone = parseJSON["phone"] as? String{
                phone = _phone
            }
            
        }
        else {
            // Woa, okay the json object was nil, something went worng. Maybe the server isn't running?
            let jsonStr = NSString(data: data, encoding: NSUTF8StringEncoding)
            println("Error could not parse JSON: \(jsonStr)")
        }
        //200 = OK
        if(status_code == 200){
            println("Valid credentials! Carry on to main page...")
            NSUserDefaults.standardUserDefaults().setObject(username, forKey: "username")
            NSUserDefaults.standardUserDefaults().setObject(first_name, forKey: "first_name")
            NSUserDefaults.standardUserDefaults().setObject(last_name, forKey: "last_name")
            NSUserDefaults.standardUserDefaults().setObject(g_email, forKey: "gonzaga_email")
            NSUserDefaults.standardUserDefaults().setObject(p_email, forKey: "pref_email")
            NSUserDefaults.standardUserDefaults().setObject(phone, forKey: "phone")
        }
        //400 = BAD_REQUEST, invalid crentials
        else if(status_code == 400){
            print("Invalid credentials")
        }
        //500 = INTERNAL_SERVER_ERROR. Oh snap *_*
        else if(status_code == 500){
            println("The server is down! Call the fire!")
        }
        else {
            println("Error in casting response, data incomplete")
        }
    }
    
    var test = NSUserDefaults.standardUserDefaults().objectForKey("username") as String
    println("test \(test)")
    
    
})

task.resume()



sleep(15)