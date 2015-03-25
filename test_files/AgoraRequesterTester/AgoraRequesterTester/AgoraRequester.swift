//
//  AgoraRequester.swift
//  AgoraRequesterTester
//
//  Created by Kyle Handy on 2/10/15.
//  Copyright (c) 2015 Kyle Handy. All rights reserved.
//

import Foundation
import SystemConfiguration

class AgoraRequester: NSObject, NSURLSessionDelegate {
    
    //base URL
    let baseURLst: String
    
    //base HTTPS url
    let baseHTTPSURLst: String
    
    //Configuration for created NSURLSessions
    let seshConfig: NSURLSessionConfiguration
    
    //default initializer, specifies the target URL
    override init(){
        self.baseURLst  = "https://cs-design.gonzaga.edu:8000/"
        self.baseHTTPSURLst = "https://cs-design.gonzaga.edu:8000/"
        self.seshConfig = NSURLSessionConfiguration.defaultSessionConfiguration()
        seshConfig.timeoutIntervalForRequest = 60
        super.init()
    }
    
    func POST(route: String, params: Dictionary<String,AnyObject>, success: ((Dictionary<String,AnyObject>) -> Void)?, failure: ((Int,String) -> Void)?){
        
        //instantiate the session
        var session = NSURLSession(configuration: self.seshConfig)
        
        //check for network connection
        if Reachability.isConnectedToNetwork(){
            
            //init request, set target URL
            var request = NSMutableURLRequest(URL: NSURL(string: self.baseURLst + route)!)
            
            //request headers: JSON -> and <-
            request.addValue("application/json", forHTTPHeaderField: "Content-Type")
            request.addValue("application/json", forHTTPHeaderField: "Accept")
            
            //AgoraRequest.POST uses method POST
            request.HTTPMethod = "POST"
            
            //load up JSON object into request body
            request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: nil)
            
            //form the task, use passed callback function
            var task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
                
                //error is not nil means there was a timeout
                if error != nil{
                    if failure != nil{
                        failure!(599,"599 connection timeout")
                    }
                }
                
                //else proceed...
                else if let httpResponse = response as? NSHTTPURLResponse{
                    
                    let status_code = httpResponse.statusCode
                    
                    //200 OK, continue as planned
                    if status_code == 200 {
                        
                        //parse the JSON response
                        var err: NSError?
                        var parseJSON = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? Dictionary<String,AnyObject>
                        
                        //error parsing
                        if err != nil {
                            //error function: 500 server failure in forming response
                            if failure != nil {
                                failure!(500,"500 server error")
                            }
                        }
                        
                        //if callback provided run callback function with provided JSON results
                        else if success != nil {
                            success!(parseJSON!)
                        }
                        
                    }
                    
                    //400 Bad Request, get error message
                    else if status_code == 400 {
                        
                        //parse the JSON response
                        var err: NSError?
                        var parseJSON = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? Dictionary<String,AnyObject>
                        
                        //error function: 400 bad request by client
                        if failure != nil {
                            let message = parseJSON!["message"] as String
                            failure!(400,message)
                        }
                    }
                    
                    //500 server failure
                    else if status_code == 500 {
                        //error function: 500 server failure by status code
                        if failure != nil {
                            failure!(500,"500 server error")
                        }
                    }
                }
                else{
                    //error function: 500 server failure by response body
                    if failure != nil {
                        failure!(500,"500 server error")
                    }
                }
            })
            
            task.resume()
            
        }
            
        //else no network connection
        else{
            //error function: 58 no connection
            if failure != nil {
                failure!(58,"58 no internet connection")
            }
        }
        
    }
    
    func LdapAuth(username: String, password: String, success: ((Dictionary<String,AnyObject>) -> Void)?, failure: ((Int,String) -> Void)?, badCreds: (Void -> Void)?){
        
        //check for network connection
        if Reachability.isConnectedToNetwork(){
        
            var request = NSMutableURLRequest(URL: NSURL(string: self.baseHTTPSURLst + "ldapauth/")!)
            request.HTTPMethod = "POST"
            
            
            var params = ["username":username, "password":password] as Dictionary<String, String>
            
            var err: NSError?
            request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: &err)
            request.addValue("application/json", forHTTPHeaderField: "Content-Type")
            request.addValue("application/json", forHTTPHeaderField: "Accept")
            
            
            var session = NSURLSession(configuration: NSURLSessionConfiguration.defaultSessionConfiguration(),
                delegate: self,
                delegateQueue:nil)
            
            
            var task = session.dataTaskWithRequest(request,completionHandler: {data, response, error -> Void in
                
                
                //error is not nil means unresponsive server (dead or timeout)
                if error != nil{
                    if failure != nil{
                        failure!(599,"599 connection timeout")
                    }
                }
                    
                //else proceed...
                else if let httpResponse = response as? NSHTTPURLResponse{
                    
                    
                    let status_code = httpResponse.statusCode
                    
                    //200 OK, continue as planned
                    if status_code == 200 {
                        println(200)
                        
                        //parse the JSON response
                        var err: NSError?
                        var parseJSON = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? Dictionary<String,AnyObject>
                        
                        //error parsing
                        if err != nil {
                            
                            //error function: 500 server failure in forming response
                            if failure != nil {
                                let message = parseJSON!["message"] as String
                                failure!(500,message)
                            }
                        }
                            
                        //if callback provided run callback function with provided JSON results
                        else if success != nil {
                            success!(parseJSON!)
                        }
                        
                    }
                        
                    //400 Bad Request, get error message
                    else if status_code == 400 {
                        println(400)
                        //error function: 400 bad request by client
                        if badCreds != nil {
                            println("400 bad request by client")
                            badCreds!()
                        }
                    }
                        
                        //500 server failure
                    else if status_code == 500 {
                        println(500)
                        //error function: 500 server failure by status code
                        if failure != nil {
                            failure!(500,"500 server failure by status code")
                        }
                    }
                    else{
                        println(status_code)
                        println("final else")
                    }
                }
                else{
                    println(500)
                    println("could not cast")
                    //error function: 500 server failure by response body
                    if failure != nil {
                        failure!(500,"500 server failure by response body")
                    }
                }
            })
            
            task.resume()
            println("task resume")
        }
        //else no network connection
        else{
            //error function: 58 no connection
            if failure != nil {
                failure!(58,"58 no connection")
            }
        }
    
    }

    func ViewPost(category: String, id: Int, info: ((Dictionary<String,AnyObject>) -> Void)?, image1: (NSData? -> Void)?, image2: (NSData? -> Void)?, image3: (NSData? -> Void)?, failure: ((Int,String) -> Void)?){
        
        //check for network connection
        if Reachability.isConnectedToNetwork(){
            
            //instantiate the session
            var session = NSURLSession(configuration: self.seshConfig)
            
            //request for post information (everything but images)
            var infoRequest = NSMutableURLRequest(URL: NSURL(string: self.baseURLst + "viewpost/")!)
            infoRequest.HTTPMethod = "POST"
            
            var params = ["category":category, "post_id":String(id)] as Dictionary<String, String>
            var err: NSError?
            infoRequest.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: &err)
            infoRequest.addValue("application/json", forHTTPHeaderField: "Content-Type")
            infoRequest.addValue("application/json", forHTTPHeaderField: "Accept")
            
            //task to gather post text
            var infoTask = session.dataTaskWithRequest(infoRequest,completionHandler: {data, response, error -> Void in
                
                
                //error is not nil means unresponsive server (dead or timeout)
                if error != nil{
                    if failure != nil{
                        failure!(599,"599 connection timeout")
                    }
                }
                    
                //else proceed...
                else if let httpResponse = response as? NSHTTPURLResponse{
                    let status_code = httpResponse.statusCode
                    //200 OK, continue as planned
                    if status_code == 200 {
                        println(200)
                        
                        //parse the JSON response
                        var err: NSError?
                        var parseJSON = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? Dictionary<String,AnyObject>
                        
                        //error parsing
                        if err != nil {
                            
                            //error function: 500 server failure in forming response
                            if failure != nil {
                                let message = parseJSON!["message"] as String
                                failure!(500,message)
                            }
                        }
                            
                        //if callback provided run callback function with provided JSON results
                        else if info != nil {
                            info!(parseJSON!)
                        }
                        
                    }
                        
                    //400 Bad Request, get error message
                    else if status_code == 400 {
                        if failure != nil{
                            failure!(400,"Bad Request")
                        }
                    }
                        
                    //500 server failure
                    else if status_code == 500 {
                        println(500)
                        //error function: 500 server failure by status code
                        if failure != nil {
                            failure!(500,"500 server failure by status code")
                        }
                    }
                    else{
                        println(status_code)
                        println("final else")
                    }
                }
                else{
                    //error function: 500 server failure by response body
                    if failure != nil {
                        failure!(500,"500 server failure by response body")
                    }
                }
            })
            
            //request for image1
            var image1Request = NSMutableURLRequest(URL: NSURL(string: self.baseURLst + "getimage/")!)
            image1Request.HTTPMethod = "POST"
            
            params = ["category":category, "post_id":String(id), "picture_id":"0"] as Dictionary<String, String>
            image1Request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: &err)
            image1Request.addValue("application/json", forHTTPHeaderField: "Content-Type")
            
            var image1Task = session.dataTaskWithRequest(image1Request,completionHandler: {data, response, error -> Void in
                
                //error is not nil means unresponsive server (dead or timeout)
                if error != nil{
                    if failure != nil{
                        failure!(599,"599 connection timeout")
                    }
                }
                    
                    //else proceed...
                else if let httpResponse = response as? NSHTTPURLResponse{
                    let status_code = httpResponse.statusCode
                    //200 OK, continue as planned
                    if status_code == 200 {
                        if image1 != nil{
                            let (parseJSON, imageData: NSData?) = self.DissectMultipart(data)
                            image1!(imageData)
                        }
                        
                    }
                    else if status_code == 204{
                        if image1 != nil{
                            image1!(nil)
                        }
                    }
                        
                        //400 Bad Request, get error message
                    else if status_code == 400 {
                        if failure != nil{
                            failure!(400,"Bad Request")
                        }
                    }
                        
                        //500 server failure
                    else if status_code == 500 {
                        println(500)
                        //error function: 500 server failure by status code
                        if failure != nil {
                            failure!(500,"500 server failure by status code")
                        }
                    }
                    else{
                        println(status_code)
                        println("final else")
                    }
                }
                else{
                    //error function: 500 server failure by response body
                    if failure != nil {
                        failure!(500,"500 server failure by response body")
                    }
                }
            })
            
            //request for image2
            var image2Request = NSMutableURLRequest(URL: NSURL(string: self.baseURLst + "getimage/")!)
            image2Request.HTTPMethod = "POST"
            
            params = ["category":category, "post_id":String(id), "picture_id":"1"] as Dictionary<String, String>
            image2Request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: &err)
            image2Request.addValue("application/json", forHTTPHeaderField: "Content-Type")
            
            var image2Task = session.dataTaskWithRequest(image2Request,completionHandler: {data, response, error -> Void in
                
                //error is not nil means unresponsive server (dead or timeout)
                if error != nil{
                    if failure != nil{
                        failure!(599,"599 connection timeout")
                    }
                }
                    
                    //else proceed...
                else if let httpResponse = response as? NSHTTPURLResponse{
                    let status_code = httpResponse.statusCode
                    //200 OK, continue as planned
                    if status_code == 200 {
                        if image2 != nil{
                            let (parseJSON, imageData: NSData?) = self.DissectMultipart(data)
                            image2!(imageData)
                        }
                        
                    }
                    else if status_code == 204{
                        if image2 != nil{
                            image2!(nil)
                        }
                    }
                        
                        //400 Bad Request, get error message
                    else if status_code == 400 {
                        if failure != nil{
                            failure!(400,"Bad Request")
                        }
                    }
                        
                        //500 server failure
                    else if status_code == 500 {
                        println(500)
                        //error function: 500 server failure by status code
                        if failure != nil {
                            failure!(500,"500 server failure by status code")
                        }
                    }
                    else{
                        println(status_code)
                        println("final else")
                    }
                }
                else{
                    //error function: 500 server failure by response body
                    if failure != nil {
                        failure!(500,"500 server failure by response body")
                    }
                }
            })
            
            //request for image2
            var image3Request = NSMutableURLRequest(URL: NSURL(string: self.baseURLst + "getimage/")!)
            image3Request.HTTPMethod = "POST"
            
            params = ["category":category, "post_id":String(id), "picture_id":"2"] as Dictionary<String, String>
            image3Request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: &err)
            image3Request.addValue("application/json", forHTTPHeaderField: "Content-Type")
            
            var image3Task = session.dataTaskWithRequest(image3Request,completionHandler: {data, response, error -> Void in
                
                //error is not nil means unresponsive server (dead or timeout)
                if error != nil{
                    if failure != nil{
                        failure!(599,"599 connection timeout")
                    }
                }
                    
                    //else proceed...
                else if let httpResponse = response as? NSHTTPURLResponse{
                    let status_code = httpResponse.statusCode
                    //200 OK, continue as planned
                    if status_code == 200 {
                        if image3 != nil{
                            let (parseJSON, imageData) = self.DissectMultipart(data)
                            image3!(imageData)
                        }
                        
                    }
                    else if status_code == 204{
                        if image3 != nil{
                            image3!(nil)
                        }
                    }
                        
                        //400 Bad Request, get error message
                    else if status_code == 400 {
                        if failure != nil{
                            failure!(400,"Bad Request")
                        }
                    }
                        
                        //500 server failure
                    else if status_code == 500 {
                        println(500)
                        //error function: 500 server failure by status code
                        if failure != nil {
                            failure!(500,"500 server failure by status code")
                        }
                    }
                    else{
                        println(status_code)
                        println("final else")
                    }
                }
                else{
                    //error function: 500 server failure by response body
                    if failure != nil {
                        failure!(500,"500 server failure by response body")
                    }
                }
            })
            
            
            infoTask.resume()
            image1Task.resume()
            image2Task.resume()
            image3Task.resume()
            
        }
        //else no network connection
        else{
            //error function: 58 no connection
            if failure != nil {
                failure!(58,"58 no connection")
            }
        }
        
    }
    
    func PostQuery(params: Dictionary<String,AnyObject>, info: ((Dictionary<String,AnyObject>) -> Void)?, imageReceived: ((String,Int,NSData) -> Void)?, failure: ((Int,String) -> Void)?){
        
        //instantiate the session
        var session = NSURLSession(configuration: self.seshConfig)
        
        //check for network connection
        if Reachability.isConnectedToNetwork(){
            
            //init request, set target URL
            var infoRequest = NSMutableURLRequest(URL: NSURL(string: self.baseURLst + "postquery/")!)
            
            //request headers: JSON -> and <-
            infoRequest.addValue("application/json", forHTTPHeaderField: "Content-Type")
            infoRequest.addValue("application/json", forHTTPHeaderField: "Accept")
            
            //AgoraRequest.POST uses method POST
            infoRequest.HTTPMethod = "POST"
            
            //load up JSON object into request body
            infoRequest.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: nil)
            
            var infoTask = session.dataTaskWithRequest(infoRequest, completionHandler: {data, response, error -> Void in
                //error is not nil means there was a timeout
                if error != nil{
                    if failure != nil{
                        failure!(599,"599 connection timeout")
                    }
                }
                
                //else proceed...
                else if let httpResponse = response as? NSHTTPURLResponse{
                
                    let status_code = httpResponse.statusCode
                
                    //200 OK/204 no content, continue as planned
                    if status_code == 200 {
                
                        //parse the JSON response
                        var err: NSError?
                        var parseJSON = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? Dictionary<String,AnyObject>
                
                        //error parsing
                        if err != nil {
                            //error function: 500 server failure in forming response
                            if failure != nil {
                                failure!(500,"500 server error")
                            }
                        }
                
                        //if callback provided run callback function with provided JSON results
                        else{
                            
                            let posts: AnyObject = parseJSON!["posts"]!
                            if posts.count > 0 {
                                for i in 0...(posts.count - 1){
                                    let post: AnyObject = posts[i]!
                                    let category = post["category"]! as String
                                    let postID = post["id"]! as Int
                                    let pictureID = "0"
                                    
                                    let imageRequest = NSMutableURLRequest(URL: NSURL(string: self.baseURLst + "getimage/")!)
                                    imageRequest.HTTPMethod = "POST"
                                    imageRequest.addValue("application/json", forHTTPHeaderField: "Content-Type")
                                    
                                    let params = ["category": category, "post_id": String(postID), "picture_id":pictureID] as Dictionary<String,AnyObject>
                                    
                                    //load up JSON object into request body
                                    imageRequest.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: nil)
                                    
                                    println("imageTask " + category + " " + String(postID))
                                    
                                    let imageTask = session.dataTaskWithRequest(imageRequest, completionHandler: {data, response, error -> Void in
                                            //error is not nil means unresponsive server (dead or timeout)
                                            if error != nil{
                                                if failure != nil{
                                                    failure!(599,"599 connection timeout")
                                                }
                                            }
                                                
                                            //else proceed...
                                            else if let httpResponse = response as? NSHTTPURLResponse{
                                                let status_code = httpResponse.statusCode
                                                //200 OK, continue as planned
                                                if status_code == 200 {
                                                    if imageReceived != nil{
                                                        let (parseJSON,imageData: NSData?) = self.DissectMultipart(data)
                                                        let postID: Int = (parseJSON["post_id"] as String).toInt()!
                                                        let category = parseJSON["category"] as String
                                                        if imageReceived != nil && imageData != nil {
                                                            imageReceived!(category,postID,imageData!)
                                                        }
                                                        else{
                                                            println("no image for " + category + " " + String(postID))
                                                        }
                                                    }
                                                }
                                                    
                                                    //400 Bad Request, get error message
                                                else if status_code == 400 {
                                                    if failure != nil{
                                                        failure!(400,"Bad Request")
                                                    }
                                                }
                                                    
                                                    //500 server failure
                                                else if status_code == 500 {
                                                    println(500)
                                                    //error function: 500 server failure by status code
                                                    if failure != nil {
                                                        failure!(500,"500 server failure by status code")
                                                    }
                                                }
                                                else{
                                                    println(status_code)
                                                    println("final else")
                                                }
                                            }
                                            else{
                                                //error function: 500 server failure by response body
                                                if failure != nil {
                                                    failure!(500,"500 server failure by response body")
                                                }
                                            }
                                        }
                                    )
                                    imageTask.resume()
                                }
                            }
                            if info != nil {
                                info!(parseJSON!)
                            }
                        }
                        
                    }
                
                    //400 Bad Request, get error message
                    else if status_code == 400 {
                
                        //parse the JSON response
                        var err: NSError?
                        var parseJSON = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? Dictionary<String,AnyObject>
                
                        //error function: 400 bad request by client
                        if failure != nil {
                            let message = parseJSON!["message"] as String
                            failure!(400,message)
                        }
                    }
                
                    //500 server failure
                    else if status_code == 500 {
                        //error function: 500 server failure by status code
                        if failure != nil {
                            failure!(500,"500 server error")
                        }
                    }
                }
                
                else{
                    //error function: 500 server failure by response body
                    if failure != nil {
                        failure!(500,"500 server error")
                    }
                }
                
                }
            )
            
            infoTask.resume()
        }
        //else no network connection
        else{
            //error function: 58 no connection
            if failure != nil {
                failure!(58,"58 no internet connection")
            }
        }
        
    }
    
    func URLSession(session: NSURLSession, didReceiveChallenge challenge: NSURLAuthenticationChallenge, completionHandler: (NSURLSessionAuthChallengeDisposition, NSURLCredential!) -> Void) {
        println("challenge")
        completionHandler(NSURLSessionAuthChallengeDisposition.UseCredential, NSURLCredential(forTrust: challenge.protectionSpace.serverTrust))
        
    }
    
    func DissectMultipart(data: NSData) -> (Dictionary<String,AnyObject>,NSData?){
        
        //convert search strings to binary data for search through response data
        let intermediateBoundaryString: NSString = "--$AGORA_boundary$"
        let intermediateBoundaryData: NSData = intermediateBoundaryString.dataUsingEncoding(NSUTF8StringEncoding)!
        let finalBoundaryString: NSString = "--$AGORA_boundary$--"
        let finalBoundaryData: NSData = finalBoundaryString.dataUsingEncoding(NSUTF8StringEncoding)!
        let bracketString: NSString = "{"
        let bracketData: NSData = bracketString.dataUsingEncoding(NSUTF8StringEncoding)!
        let bracket2String: NSString = "}"
        let bracket2Data: NSData = bracket2String.dataUsingEncoding(NSUTF8StringEncoding)!
        let imageContentString: NSString = "Content-Type: image/png"
        let imageContentData: NSData = imageContentString.dataUsingEncoding(NSUTF8StringEncoding)!
        
        //find json range by searching for { }
        let bracketRange: NSRange = data.rangeOfData(bracketData, options: nil, range: NSMakeRange(0, data.length))
        let bracket2Range: NSRange = data.rangeOfData(bracket2Data, options: nil, range: NSMakeRange(0, data.length))
        
        
        //extract json data from response body
        let jsonRange: NSRange = NSUnionRange(bracketRange, bracket2Range)
        let jsonData: NSData = data.subdataWithRange(jsonRange)
        var parseJSON = NSJSONSerialization.JSONObjectWithData(jsonData, options: NSJSONReadingOptions(0), error: nil) as Dictionary<String,AnyObject>
        
        
        let imageFlag = parseJSON["image"] as Bool
        
        var imageData: NSData?
        if imageFlag{
            let imageBoundaryRange: NSRange = data.rangeOfData(imageContentData, options: nil, range: NSMakeRange(jsonRange.location, data.length - jsonRange.location))
            
            let finalBoundaryRange: NSRange = data.rangeOfData(finalBoundaryData, options: nil, range: NSMakeRange(0, data.length))
            
            let imageLocation = imageBoundaryRange.location + imageBoundaryRange.length + 4 // +2 ?
            let imageLength = finalBoundaryRange.location - imageLocation - 0
            let imageRange: NSRange = NSMakeRange(imageLocation, imageLength)
            
            imageData = data.subdataWithRange(imageRange)
        }
        else{
            imageData = nil
        }
        return (parseJSON,imageData)
    }
    
    
}



//Reachability class will tell us if there is a network connection
public class Reachability {
    
    class func isConnectedToNetwork() -> Bool {
        
        var zeroAddress = sockaddr_in(sin_len: 0, sin_family: 0, sin_port: 0, sin_addr: in_addr(s_addr: 0), sin_zero: (0, 0, 0, 0, 0, 0, 0, 0))
        zeroAddress.sin_len = UInt8(sizeofValue(zeroAddress))
        zeroAddress.sin_family = sa_family_t(AF_INET)
        
        let defaultRouteReachability = withUnsafePointer(&zeroAddress) {
            SCNetworkReachabilityCreateWithAddress(nil, UnsafePointer($0)).takeRetainedValue()
        }
        
        var flags: SCNetworkReachabilityFlags = 0
        if SCNetworkReachabilityGetFlags(defaultRouteReachability, &flags) == 0 {
            return false
        }
        
        let isReachable = (flags & UInt32(kSCNetworkFlagsReachable)) != 0
        let needsConnection = (flags & UInt32(kSCNetworkFlagsConnectionRequired)) != 0
        
        return (isReachable && !needsConnection) ? true : false
    }
    
}

