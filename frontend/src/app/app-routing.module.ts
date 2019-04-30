import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';


import {LayoutComponent} from './dashboard/layout/layout.component'
import { PageComponent } from './landing-page/page/page.component';
const routes: Routes = [
	{
		path: 'landing-page',
		component: PageComponent
	},
	{ path: '', redirectTo: 'agent/dashboard', pathMatch: 'full' },
	// 404 page
	{
		path: '**',
		redirectTo: 'dashboard'
	}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
