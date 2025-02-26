import 'zone.js/dist/zone-node';

import {APP_BASE_HREF} from '@angular/common';
import { RESPONSE } from '@nguniversal/express-engine/tokens';
import {ngExpressEngine} from '@nguniversal/express-engine';
import * as express from 'express';
import {existsSync} from 'fs';
import {join} from 'path';

import {AppServerModule} from './src/main.server';
import { environment } from 'src/environments/environment';

interface APIResponse {
  id: number,
  longUrl: string,
  shortUrl: string,
  img_svg: string,
  ip_user: string,
}

async function getFromAPI(endpoint: string) {
  let response = await fetch(environment.API_URL + "/" + endpoint);
  let json = await response.json();
  return json;
}

// The Express app is exported so that it can be used by serverless Functions.
export function app(): express.Express {
  const server = express();
  const distFolder = join(process.cwd(), 'dist/angular-short-url/browser');
  const indexHtml = existsSync(join(distFolder, 'index.original.html')) ? 'index.original.html' : 'index';

  // Our Universal express-engine (found @ https://github.com/angular/universal/tree/main/modules/express-engine)
  server.engine('html', ngExpressEngine({
    bootstrap: AppServerModule,
  }));

  server.set('view engine', 'html');
  server.set('views', distFolder);

  // Example Express Rest API endpoints
  // server.get('/api/**', (req, res) => { });
  // Serve static files from /browser
  server.get('*.*', express.static(distFolder, {
    maxAge: '1y'
  }));

  // All regular routes use the Universal engine
  server.get(/^\/.{4}$/, async (req, res) => {
    const code = req.url.substring(req.url.length - 4);
    try {
      //console.log(code);
      const value = await getFromAPI(`/grs/${code}`) as APIResponse;
      if (value.longUrl) {
        res.redirect(value.longUrl);
      } else {
        res.status(404).render(indexHtml, { req, providers: [{ provide: APP_BASE_HREF, useValue: req.baseUrl }, { provide: RESPONSE, useValue: res }] });
      }
    } catch (e) {
      res.status(500).send("Ошибка сервера: " + e);
    }
  });

  server.get('*', (req, res) => {
    res.render(indexHtml, { req, providers: [{ provide: APP_BASE_HREF, useValue: req.baseUrl }, { provide: RESPONSE, useValue: res }] });
  });

  return server;
}

function run(): void {
  const port = process.env['PORT'] || 4000;

  // Start up the Node server
  const server = app();
  server.listen(port, () => {
    console.log(`Node Express server listening on http://localhost:${port}`);
  });
}

// Webpack will replace 'require' with '__webpack_require__'
// '__non_webpack_require__' is a proxy to Node 'require'
// The below code is to ensure that the server is run only when not requiring the bundle.
declare const __non_webpack_require__: NodeRequire;
const mainModule = __non_webpack_require__.main;
const moduleFilename = mainModule && mainModule.filename || '';
if (moduleFilename === __filename || moduleFilename.includes('iisnode')) {
  run();
}

export * from './src/main.server';
