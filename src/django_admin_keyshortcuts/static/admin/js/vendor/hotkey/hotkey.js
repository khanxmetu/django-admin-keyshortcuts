class Leaf {
    constructor(trie) {
        this.children = [];
        this.parent = trie;
    }
    delete(value) {
        const index = this.children.indexOf(value);
        if (index === -1)
            return false;
        this.children = this.children.slice(0, index).concat(this.children.slice(index + 1));
        if (this.children.length === 0) {
            this.parent.delete(this);
        }
        return true;
    }
    add(value) {
        this.children.push(value);
        return this;
    }
}
class RadixTrie {
    constructor(trie) {
        this.parent = null;
        this.children = {};
        this.parent = trie || null;
    }
    get(edge) {
        return this.children[edge];
    }
    insert(edges) {
        let currentNode = this;
        for (let i = 0; i < edges.length; i += 1) {
            const edge = edges[i];
            let nextNode = currentNode.get(edge);
            if (i === edges.length - 1) {
                if (nextNode instanceof RadixTrie) {
                    currentNode.delete(nextNode);
                    nextNode = null;
                }
                if (!nextNode) {
                    nextNode = new Leaf(currentNode);
                    currentNode.children[edge] = nextNode;
                }
                return nextNode;
            }
            else {
                if (nextNode instanceof Leaf)
                    nextNode = null;
                if (!nextNode) {
                    nextNode = new RadixTrie(currentNode);
                    currentNode.children[edge] = nextNode;
                }
            }
            currentNode = nextNode;
        }
        return currentNode;
    }
    delete(node) {
        for (const edge in this.children) {
            const currentNode = this.children[edge];
            if (currentNode === node) {
                const success = delete this.children[edge];
                if (Object.keys(this.children).length === 0 && this.parent) {
                    this.parent.delete(this);
                }
                return success;
            }
        }
        return false;
    }
}

const macosSymbolLayerKeys = {
    ['¡']: '1',
    ['™']: '2',
    ['£']: '3',
    ['¢']: '4',
    ['∞']: '5',
    ['§']: '6',
    ['¶']: '7',
    ['•']: '8',
    ['ª']: '9',
    ['º']: '0',
    ['–']: '-',
    ['≠']: '=',
    ['⁄']: '!',
    ['€']: '@',
    ['‹']: '#',
    ['›']: '$',
    ['ﬁ']: '%',
    ['ﬂ']: '^',
    ['‡']: '&',
    ['°']: '*',
    ['·']: '(',
    ['‚']: ')',
    ['—']: '_',
    ['±']: '+',
    ['œ']: 'q',
    ['∑']: 'w',
    ['®']: 'r',
    ['†']: 't',
    ['¥']: 'y',
    ['ø']: 'o',
    ['π']: 'p',
    ['“']: '[',
    ['‘']: ']',
    ['«']: '\\',
    ['Œ']: 'Q',
    ['„']: 'W',
    ['´']: 'E',
    ['‰']: 'R',
    ['ˇ']: 'T',
    ['Á']: 'Y',
    ['¨']: 'U',
    ['ˆ']: 'I',
    ['Ø']: 'O',
    ['∏']: 'P',
    ['”']: '{',
    ['’']: '}',
    ['»']: '|',
    ['å']: 'a',
    ['ß']: 's',
    ['∂']: 'd',
    ['ƒ']: 'f',
    ['©']: 'g',
    ['˙']: 'h',
    ['∆']: 'j',
    ['˚']: 'k',
    ['¬']: 'l',
    ['…']: ';',
    ['æ']: "'",
    ['Å']: 'A',
    ['Í']: 'S',
    ['Î']: 'D',
    ['Ï']: 'F',
    ['˝']: 'G',
    ['Ó']: 'H',
    ['Ô']: 'J',
    ['']: 'K',
    ['Ò']: 'L',
    ['Ú']: ':',
    ['Æ']: '"',
    ['Ω']: 'z',
    ['≈']: 'x',
    ['ç']: 'c',
    ['√']: 'v',
    ['∫']: 'b',
    ['µ']: 'm',
    ['≤']: ',',
    ['≥']: '.',
    ['÷']: '/',
    ['¸']: 'Z',
    ['˛']: 'X',
    ['Ç']: 'C',
    ['◊']: 'V',
    ['ı']: 'B',
    ['˜']: 'N',
    ['Â']: 'M',
    ['¯']: '<',
    ['˘']: '>',
    ['¿']: '?'
};

const macosUppercaseLayerKeys = {
    ['`']: '~',
    ['1']: '!',
    ['2']: '@',
    ['3']: '#',
    ['4']: '$',
    ['5']: '%',
    ['6']: '^',
    ['7']: '&',
    ['8']: '*',
    ['9']: '(',
    ['0']: ')',
    ['-']: '_',
    ['=']: '+',
    ['[']: '{',
    [']']: '}',
    ['\\']: '|',
    [';']: ':',
    ["'"]: '"',
    [',']: '<',
    ['.']: '>',
    ['/']: '?',
    ['q']: 'Q',
    ['w']: 'W',
    ['e']: 'E',
    ['r']: 'R',
    ['t']: 'T',
    ['y']: 'Y',
    ['u']: 'U',
    ['i']: 'I',
    ['o']: 'O',
    ['p']: 'P',
    ['a']: 'A',
    ['s']: 'S',
    ['d']: 'D',
    ['f']: 'F',
    ['g']: 'G',
    ['h']: 'H',
    ['j']: 'J',
    ['k']: 'K',
    ['l']: 'L',
    ['z']: 'Z',
    ['x']: 'X',
    ['c']: 'C',
    ['v']: 'V',
    ['b']: 'B',
    ['n']: 'N',
    ['m']: 'M'
};

const syntheticKeyNames = {
    ' ': 'Space',
    '+': 'Plus'
};
function eventToHotkeyString(event, platform = navigator.platform) {
    var _a, _b, _c;
    const { ctrlKey, altKey, metaKey, shiftKey, key } = event;
    const hotkeyString = [];
    const modifiers = [ctrlKey, altKey, metaKey, shiftKey];
    for (const [i, mod] of modifiers.entries()) {
        if (mod)
            hotkeyString.push(modifierKeyNames[i]);
    }
    if (!modifierKeyNames.includes(key)) {
        const altNormalizedKey = hotkeyString.includes('Alt') && matchApplePlatform.test(platform) ? (_a = macosSymbolLayerKeys[key]) !== null && _a !== void 0 ? _a : key : key;
        const shiftNormalizedKey = hotkeyString.includes('Shift') && matchApplePlatform.test(platform)
            ? (_b = macosUppercaseLayerKeys[altNormalizedKey]) !== null && _b !== void 0 ? _b : altNormalizedKey
            : altNormalizedKey;
        const syntheticKey = (_c = syntheticKeyNames[shiftNormalizedKey]) !== null && _c !== void 0 ? _c : shiftNormalizedKey;
        hotkeyString.push(syntheticKey);
    }
    return hotkeyString.join('+');
}
const modifierKeyNames = ['Control', 'Alt', 'Meta', 'Shift'];
function normalizeHotkey(hotkey, platform) {
    let result;
    result = localizeMod(hotkey, platform);
    result = sortModifiers(result);
    return result;
}
const matchApplePlatform = /Mac|iPod|iPhone|iPad/i;
function localizeMod(hotkey, platform) {
    var _a;
    const ssrSafeWindow = typeof window === 'undefined' ? undefined : window;
    const safePlatform = (_a = platform !== null && platform !== void 0 ? platform : ssrSafeWindow === null || ssrSafeWindow === void 0 ? void 0 : ssrSafeWindow.navigator.platform) !== null && _a !== void 0 ? _a : '';
    const localModifier = matchApplePlatform.test(safePlatform) ? 'Meta' : 'Control';
    return hotkey.replace('Mod', localModifier);
}
function sortModifiers(hotkey) {
    const key = hotkey.split('+').pop();
    const modifiers = [];
    for (const modifier of ['Control', 'Alt', 'Meta', 'Shift']) {
        if (hotkey.includes(modifier)) {
            modifiers.push(modifier);
        }
    }
    if (key)
        modifiers.push(key);
    return modifiers.join('+');
}

const SEQUENCE_DELIMITER = ' ';
class SequenceTracker {
    constructor({ onReset } = {}) {
        this._path = [];
        this.timer = null;
        this.onReset = onReset;
    }
    get path() {
        return this._path;
    }
    get sequence() {
        return this._path.join(SEQUENCE_DELIMITER);
    }
    registerKeypress(event) {
        this._path = [...this._path, eventToHotkeyString(event)];
        this.startTimer();
    }
    reset() {
        var _a;
        this.killTimer();
        this._path = [];
        (_a = this.onReset) === null || _a === void 0 ? void 0 : _a.call(this);
    }
    killTimer() {
        if (this.timer != null) {
            window.clearTimeout(this.timer);
        }
        this.timer = null;
    }
    startTimer() {
        this.killTimer();
        this.timer = window.setTimeout(() => this.reset(), SequenceTracker.CHORD_TIMEOUT);
    }
}
SequenceTracker.CHORD_TIMEOUT = 1500;
function normalizeSequence(sequence) {
    return sequence
        .split(SEQUENCE_DELIMITER)
        .map(h => normalizeHotkey(h))
        .join(SEQUENCE_DELIMITER);
}

function isFormField(element) {
    if (!(element instanceof HTMLElement)) {
        return false;
    }
    const name = element.nodeName.toLowerCase();
    const type = (element.getAttribute('type') || '').toLowerCase();
    return (name === 'select' ||
        name === 'textarea' ||
        (name === 'input' &&
            type !== 'submit' &&
            type !== 'reset' &&
            type !== 'checkbox' &&
            type !== 'radio' &&
            type !== 'file') ||
        element.isContentEditable);
}
function fireDeterminedAction(el, path) {
    const delegateEvent = new CustomEvent('hotkey-fire', { cancelable: true, detail: { path } });
    const cancelled = !el.dispatchEvent(delegateEvent);
    if (cancelled)
        return;
    if (isFormField(el)) {
        el.focus();
    }
    else {
        el.click();
    }
}
function expandHotkeyToEdges(hotkey) {
    const output = [];
    let acc = [''];
    let commaIsSeparator = false;
    for (let i = 0; i < hotkey.length; i++) {
        if (commaIsSeparator && hotkey[i] === ',') {
            output.push(acc);
            acc = [''];
            commaIsSeparator = false;
            continue;
        }
        if (hotkey[i] === SEQUENCE_DELIMITER) {
            acc.push('');
            commaIsSeparator = false;
            continue;
        }
        else if (hotkey[i] === '+') {
            commaIsSeparator = false;
        }
        else {
            commaIsSeparator = true;
        }
        acc[acc.length - 1] += hotkey[i];
    }
    output.push(acc);
    return output.map(h => h.map(k => normalizeHotkey(k)).filter(k => k !== '')).filter(h => h.length > 0);
}

const hotkeyRadixTrie = new RadixTrie();
const elementsLeaves = new WeakMap();
let currentTriePosition = hotkeyRadixTrie;
const sequenceTracker = new SequenceTracker({
    onReset() {
        currentTriePosition = hotkeyRadixTrie;
    }
});
function keyDownHandler(event) {
    if (event.defaultPrevented)
        return;
    if (!(event.target instanceof Node))
        return;
    if (isFormField(event.target)) {
        const target = event.target;
        if (!target.id)
            return;
        if (!target.ownerDocument.querySelector(`[data-hotkey-scope="${target.id}"]`))
            return;
    }
    const newTriePosition = currentTriePosition.get(eventToHotkeyString(event));
    if (!newTriePosition) {
        sequenceTracker.reset();
        return;
    }
    sequenceTracker.registerKeypress(event);
    currentTriePosition = newTriePosition;
    if (newTriePosition instanceof Leaf) {
        const target = event.target;
        let shouldFire = false;
        let elementToFire;
        const formField = isFormField(target);
        for (let i = newTriePosition.children.length - 1; i >= 0; i -= 1) {
            elementToFire = newTriePosition.children[i];
            const scope = elementToFire.getAttribute('data-hotkey-scope');
            if ((!formField && !scope) || (formField && target.id === scope)) {
                shouldFire = true;
                break;
            }
        }
        if (elementToFire && shouldFire) {
            fireDeterminedAction(elementToFire, sequenceTracker.path);
            event.preventDefault();
        }
        sequenceTracker.reset();
    }
}
function install(element, hotkey) {
    if (Object.keys(hotkeyRadixTrie.children).length === 0) {
        document.addEventListener('keydown', keyDownHandler);
    }
    const hotkeys = expandHotkeyToEdges(hotkey || element.getAttribute('data-hotkey') || '');
    const leaves = hotkeys.map(h => hotkeyRadixTrie.insert(h).add(element));
    elementsLeaves.set(element, leaves);
}
function uninstall(element) {
    const leaves = elementsLeaves.get(element);
    if (leaves && leaves.length) {
        for (const leaf of leaves) {
            leaf && leaf.delete(element);
        }
    }
    if (Object.keys(hotkeyRadixTrie.children).length === 0) {
        document.removeEventListener('keydown', keyDownHandler);
    }
}

export { Leaf, RadixTrie, SequenceTracker, eventToHotkeyString, install, normalizeHotkey, normalizeSequence, uninstall };