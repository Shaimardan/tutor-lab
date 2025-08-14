import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiModule } from './openapi/api.module';

import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';
import { PagesModule } from './pages/pages.module';

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    ApiModule.forRoot({ rootUrl: '/api' }),
    MatButtonModule,
    MatDividerModule,
    PagesModule,
  ],
  providers: [MatDividerModule],
  exports: [MatDividerModule],
  bootstrap: [],
})
export class AppModule {}
