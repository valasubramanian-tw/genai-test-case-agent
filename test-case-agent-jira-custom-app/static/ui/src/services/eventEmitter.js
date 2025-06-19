class EventEmitter extends EventTarget {
    emit(eventName, data) {
        const event = new CustomEvent(eventName, { detail: data });
        this.dispatchEvent(event);
    }
}

export const eventEmitter = new EventEmitter();
export const EVENT_TYPES = {
    TEST_CASE_CHUNK: 'TEST_CASE_CHUNK',
    TEST_CASE_ERROR: 'TEST_CASE_ERROR',
    TEST_CASE_COMPLETE: 'TEST_CASE_COMPLETE'
};