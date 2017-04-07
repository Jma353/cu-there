let initialDetailState = {};
export function _detail (state = initialDetailState, action) {
  switch (action.type) {
    // On showing the detail view
    case 'DID_SHOW_DETAIL':
      return {
        ...state,
        detail: action.detail
      };
    // On hiding the detail view
    case 'DID_HIDE_DETAIL':
      return {
        ...state,
        detail: null
      }
    // Default, catch all
    default:
      return state;
  }
}
