import { isWebview } from "./constant"

const shuntSpawner = (handleWebview) => (handleDesktop) =>
  isWebview ? handleWebview : handleDesktop;

export default shuntSpawner;
