import React from 'react';
import * as ReactDOMClient from 'react-dom/client';


const container = document.getElementById(VISUALIZER_INSTANCE_ID);
const root = ReactDOMClient.createRoot(container);
const onUpdateFromControl = (descriptor) => {
    console.log('rendering', descriptor);
    root.render(<p>Hello WORLD!</p>);
}
console.log('connecting to control');
WEBGME_CONTROL.registerUpdate(onUpdateFromControl);