import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import {IntentsComponent} from './intents/intents.component';
import {QuestionComponent} from './question/question.component';

import {IntentComponent} from './intent/intent.component';
import {TrainComponent} from './train/train.component';
import {SettingsComponent} from './settings/settings.component';
import {ChatComponent} from './chat/chat.component';
import {EntitiesComponent} from './entities/entities.component'
import {EntityComponent} from './entity/entity.component'
import {EntityResolverService} from '../services/entities.service'
import {IntentResolverService} from '../services/intent-resolver.service';
import { PageComponent } from '../landing-page/page/page.component';
import {LayoutComponent} from '../dashboard/layout/layout.component'
import {QuestionListComponent} from './question-list/question-list.component';
import { QuestionResolverService } from '../services/question-resolver.service';



const routes: Routes = [
  {
		path: 'agent',
    component: PageComponent,
    children: [
      {
        path: 'intents', component: IntentsComponent,
      },
      {
        path: 'dashboard', component: LayoutComponent,
      },
      {
        path: 'create_question', component: QuestionComponent,
      },
      {
        path: 'create-intent', component: IntentComponent,
      },
      {
        resolve: {
          story: IntentResolverService,
        },
        path: 'edit-intent/:intent_id',
         component: IntentComponent,
      },
      {
        resolve: {
          story: QuestionResolverService,
        },
        path: 'edit_question/:question_id',
        component: QuestionComponent
      },
      {
        path: 'entities', component: EntitiesComponent,
      },
      {
        resolve: {
          entity: EntityResolverService,
        },
        path: 'edit-entity/:entity_id', component: EntityComponent,
      },
      {
        resolve: {
          story: IntentResolverService,
        },
        path: 'train-intent/:intent_id', component: TrainComponent,
      },
      {
        path: 'settings', component: SettingsComponent,
      },
      {
        path: 'chat', component: ChatComponent,
      },

      {
        path: 'question_list',
        component: QuestionListComponent
      },
      {
        path: 'question',
        component: QuestionComponent
      },

      { path: '', redirectTo: 'intents', pathMatch: 'full'}
    ]
	},
  
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AgentRoutingModule { }
