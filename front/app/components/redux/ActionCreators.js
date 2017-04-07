export function didShowDetail (detail) {
  return {
    type: 'DID_SHOW_DETAIL',
    detail: detail
  };
}

export function didHideDetail () {
  return {
    type: 'DID_HIDE_DETAIL'
  };
}
