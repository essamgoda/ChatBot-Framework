import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PageComponent } from './landing-page/page/page.component';
import { AngularFontAwesomeModule } from 'angular-font-awesome';
/* Material UI imports begins here */
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatIconModule,MatCardModule,MatInputModule,
  MatOptionModule,MatSelectModule,MatCheckboxModule,MatButtonModule, MatToolbarModule} from '@angular/material';
import {MatGridListModule} from '@angular/material/grid-list';
import {MatDividerModule} from '@angular/material/divider';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatSliderModule} from '@angular/material/slider';
import {MatChipsModule} from '@angular/material/chips';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import {FlexLayoutModule} from "@angular/flex-layout";
// import { ChartsModule } from 'ng2-charts';
  
  /* Material UI imports ends here */

/* Project Modules imports begins here */
import {CommonsModule} from './commons/commons.module'
import { DashboardModule } from './dashboard/dashboard.module';
import { AgentModule } from './agent/agent.module';
// import { QuestionListComponent } from './agent/question-list/question-list.component';
/* Project Modules imports ends here */


@NgModule({
  declarations: [
    AppComponent,
    PageComponent,
    // QuestionListComponent
  ],
  imports: [
    BrowserModule,
    AgentModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    CommonsModule.forRoot(),
    DashboardModule,
    MatSidenavModule,
    MatIconModule,
    MatCardModule,
    MatInputModule,
    MatOptionModule,
    MatSelectModule,
    MatCheckboxModule,
    MatButtonModule,
    MatGridListModule,
    MatDividerModule,
    MatExpansionModule,
    MatSliderModule,
    MatChipsModule,
    FlexLayoutModule,
    MatToolbarModule,
    MatAutocompleteModule,
    AngularFontAwesomeModule,
    MatProgressSpinnerModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
