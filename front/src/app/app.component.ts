import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, NavigationEnd, Router, RouterState, RoutesRecognized } from '@angular/router';
import { Observable } from 'rxjs';
import { filter, map } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  previousUrl: string = '';
  currentUrl: string = '';
  constructor(private router: Router, route: ActivatedRoute) {    
    console.log('document.referrer-->');
    console.log(document.referrer);
  }
  
  ngOnInit(): void {    
  }

}
